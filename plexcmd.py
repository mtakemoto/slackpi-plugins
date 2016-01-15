from plexapi.server import PlexServer
from plugin_base import Plugin
import random

outputs = []
plex = PlexServer('http://localhost:32400')
plugin = Plugin()

def format_list(list):
    return ''.join(list)

def listall(argv, channel):
    list = []
    sectitle = argv[2]
    for show in plex.library.section(sectitle).all():
        list.append(show.title + '\n')
    plugin.reply(format_list(list), channel, outputs)
    return None

def setplayer(argv, channel):
    list = []
    for client in plex.clients():
        list.append(client.name + '\n')
    plugin.reply(format_list(list), channel, outputs)
    return None

def get_section_list(secname):
    list = []
    for item in plex.library.section(secname).all():
        list.append(item.title)
    return list

def get_libraries_list():
    libs = []
    for section in plex.library.sections():
        libs.append(section.title)
    return libs

def shuffle(argv, channel):
    liblist = get_libraries_list()
    if len(argv) < 3:
        plugin.reply("Usage: plexcmd shuffle <library or show name>", channel, outputs)
        return
    else:
        target = argv[2]
        if target in liblist:
            seclist = get_section_list(target)
            section = plex.library.section(target)
            random_item = random.choice(seclist) 
            if section.TYPE == 'movie':
                movie = plex.library.get(random_item)
                plugin.reply(movie.title, channel, outputs)
            elif section.TYPE == 'show':
                show = plex.library.get(random_item)
                episode = random.choice(show.episodes())
                plugin.reply("%s \"%s\"" % (show.title, episode.title), channel, outputs)
    return

def process_message(data):
    channel = data["channel"]
    text = data["text"]

    #DM only
    if channel.startswith("D"):
        if text.startswith("plexcmd"):
            argv = text.split()

            options = {"list" : listall,
                       "setplayer" : setplayer,
                        "shuffle" : shuffle,
            }
            options[argv[1]](argv, channel)

    return None


#argv = ['plexcmd', 'shuffle', 'Movies']
#channel = 'DM12345'
#shuffle(argv, channel)

#shows = plex.library.section(shows)
#showsize = len(shows)
#random.randint(0, showsize - 1)
    '''Planned functions:
        list <library>
        shuffle <library> <show, if one> [-p]
            --"plex shuffle Shows"
            --"plex shuffle Adventure Time"

        setplayer
            --list connected devices & respond with number
            --respond within 30 secs  or with 'cancel' to cancel
        plexcmd
            --print usage and availible functions

    '''



