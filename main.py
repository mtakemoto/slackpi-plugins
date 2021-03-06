import shlex
import thread
import time
import sys, threading
from evdev import InputDevice, list_devices, ecodes
from slackpi_base import * 
from plexcmd import PlexCMD
from detect import Detect
from weather import Weather

#Set joystick button mapping based on physical orientation
JS_UP = ecodes.KEY_LEFT
JS_DOWN = ecodes.KEY_RIGHT 
JS_LEFT = ecodes.KEY_DOWN 
JS_RIGHT = ecodes.KEY_UP 

#initialize all helper classes
slack = Slack()
sensehat = SenseHatWrap()
plex = PlexCMD()
weather = Weather("98225")
weather.get_current()
weather.report()

#Set local outputs array
outputs = []
crontable = []

#Cron Jobs

#-----------------------------------
def process_message(data):
    channel = data["channel"]
    text = data["text"]
    argv = shlex.split(text)
    command = ""
    
    if(argv):
        command = argv[0].lower()

    #DM only
    if channel.startswith("D"):
        if command == "plex": 
            if len(argv) < 2:
                slack.reply("plex <list> <setplayer> <shuffle> <refresh>", channel, outputs)
                return None
            options = {"list" : plex.listall,
                       "setplayer" : plex.setplayer,
                       "shuffle" : plex.shuffle,
                       "refresh" : plex.refresh,
            }
            if argv[1] in options:
                options[argv[1]](argv, channel)
        elif command == "detect":
            detect.status(argv, channel)
        elif command == "message":
            if(len(argv) == 2):
                sensehat.print_message(argv[1])
            else:
                slack.reply("Usage: message \"message here\"")
        elif command == "weather":
            if len(argv) < 2:
                slack.reply("weather <report>", channel, outputs)
                return None
            options = {"report" : weather.report,
                      }
            if argv[1] in options:
                response = options[argv[1]](argv)
                slack.reply(response, channel, outputs)
            

    return None


class JoystickListener(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def handle_code(self, code, action):
        if code == JS_DOWN: 
            return
        elif code == JS_UP:
            return
        elif code == JS_LEFT:
            return
        elif code == JS_RIGHT: 
            sensehat.print_message(weather.report_basic())
        elif code == ecodes.KEY_ENTER:
            return

    def run(self):
        print "Starting " + self.name
        running = True
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:  # key down
                    print("key down")
                    self.handle_code(event.code, "down")
                '''if event.value == 0:  # key up
                    print("key up")
                    self.handle_code(event.code, "up")
                '''
#----------------------------

found = False
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True
        break

if found:
    js_listener = JoystickListener("Hat JS Listener")
    js_listener.start()
else:
    print "Critical Error: Sense Hat Joystick not found"

