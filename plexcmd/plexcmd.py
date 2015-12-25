from plexapi.server import PlexServer
import random

plex = PlexServer('http://192.168.0.110:32400')
outputs = []
contable = []

def reply(message, channel):
    outputs.append([channel, message])
    return None

def format_list(list):
    return ''.join(list)

def listall(argv, channel):
    list = []
    sectitle = argv[2]
    for show in plex.library.section(sectitle).all():
        list.append(show.title + '\n')
    reply(format_list(list), channel)
    return None

def setplayer(argv, channel):
    list = []
    for client in plex.clients():
        list.append(client.name + '\n')
    reply(format_list(list), channel)
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
        reply("Usage: plexcmd shuffle <library or show name>", channel)
        return
    else:
        target = argv[2]
        if target in liblist:
            seclist = get_section_list(target)
            section = plex.library.section(target)
            random_item = seclist[random.randint(0, len(seclist) - 1)]
            if section.TYPE == 'movie':
                movie = plex.library.get(random_item)
                reply(movie.title, channel)
            elif section.TYPE == 'show':
                show = plex.library.get(random_item)
                reply(show.title, channel)
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



