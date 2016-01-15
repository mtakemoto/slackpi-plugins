from plexapi.server import PlexServer
from plexapi.client import Client
from plugin_base import Plugin
import random
import shlex
import traceback

outputs = []
plex = PlexServer('http://localhost:32400')
player = Client(plex, plex.query('/clients'))
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

def list_players(argv, channel):
    clients = plex.clients()
    if not clients:
        plugin.reply("no players connected", channel, outputs)
        return None
    for idx, client in enumerate(plex.clients()):
        response = "[%i] %s \n" % ((idx + 1), client.name)
        plugin.reply(response, channel, outputs)

def setplayer(argv, channel):
    clients = plex.clients()
    if len(argv) > 2 and argv[2].isdigit() and int(argv[2]) <= len(plex.clients()):
        if clients:
            clinum = int(argv[2])
            global player
            player = plex.clients()[clinum - 1] 
            plugin.reply("Player set to %s" % player.name, channel, outputs)
        else:
            plugin.reply("Error: no clients", channel, outputs)
    else:
        plugin.reply("Usage: plexcmd setplayer <player ID>", channel, outputs)
    return None

def play(media, channel):
    if player.name:
        player.playMedia(media)
    else:
        plugin.reply("Error: player not set or disconnected", channel, outputs)

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

def shuffle_movies(movie, channel):
    plugin.reply(movie.title, channel, outputs)

def shuffle_shows(show, channel):
    episode = random.choice(show.episodes())
    plugin.reply("%s \"%s\"" % (show.title, episode.title), channel, outputs)

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
            random_item = plex.library.get(random.choice(seclist))
            if section.TYPE == 'movie':
                shuffle_movies(random_item, channel)
            elif section.TYPE == 'show':
                shuffle_shows(random_item, channel)
            if argv[-1] == "-p":
                play(random_item, channel)
    return

def process_message(data):
    try:
        channel = data["channel"]
        text = data["text"]

        #DM only
        if channel.startswith("D"):
            if text.startswith("plexcmd"):
                argv = shlex.split(text)

                options = {"list" : listall,
                           "setplayer" : setplayer,
                           "listplayers": list_players,
                           "shuffle" : shuffle,
                }
                options[argv[1]](argv, channel)

    except Exception, error:
        print "%s: %s" % (error.__doc__, error.name)
        traceback.print_exec()
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



