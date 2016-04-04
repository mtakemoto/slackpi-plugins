import shlex
import thread
import time
from slackpi_base import SlackPi 
from plexcmd import PlexCMD
from detect import Detect
from weather import Weather

#initialize all helper classes
slackpi = SlackPi()
plex = PlexCMD()
weather = Weather("98225")
weather.get_current()
weather.report()

#Set local outputs array
outputs = []
crontable = []

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
                slackpi.reply("plex <list> <setplayer> <shuffle> <refresh>", channel, outputs)
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
            slackpi.print_message(argv, channel)

    return None
