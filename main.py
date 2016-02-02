import shlex
from slackpi_base import SlackPi 
from plexcmd import PlexCMD

#initialize all helper classes
slackpi = SlackPi()
plex = PlexCMD()

#Set local outputs array
outputs = []

def process_message(data):
    print data

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
        if command == "message": 
            slackpi.sense.show_message(argv[1])
    return None
