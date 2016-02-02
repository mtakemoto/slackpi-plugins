import shlex
from plugin_base import Plugin
from plexcmd import PlexCMD

#initialize all helper classes
plugin = Plugin()
plex = PlexCMD()

#Set local outputs array
outputs = []

def process_message(data):
    print "process message called in plexcmd.py"

    channel = data["channel"]
    text = data["text"]
    argv = shlex.split(text)

    #DM only
    if channel.startswith("D"):
        if text.lower().startswith("plex"):
            if len(argv) < 2:
                plugin.reply("plex <list> <setplayer> <shuffle> <refresh>", channel, outputs)
                return None
            options = {"list" : plex.list,
                       "setplayer" : plex.setplayer,
                       "shuffle" : plex.shuffle,
                       "refresh" : plex.refresh,
            }
            options[argv[1]](argv, channel)
        if text.lower().startswith("message"):
            plugin.sense.show_message(argv[1])
    return None
