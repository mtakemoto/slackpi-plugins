from plexapi.server import PlexServer
from plexapi.client import Client
from plugin_base import Plugin
import random
import shlex
import traceback
import time

outputs = []
plugin = Plugin()

retries = 0
while retries < 5:
    try:
        plex = PlexServer('http://localhost:32400')
        player = Client(plex, plex.query('/clients'))
        break
    except Exception:
        print "Error: server not found.  Retrying..."
        retries += 1
    time.sleep(5)

def format_list(list):
    return ''.join(list)

def list(argv, channel):
    list = []
    param = argv[2]
    if param in get_libraries_list():
        for show in plex.library.section(param).all():
            list.append(show.title + '\n')
        plugin.reply(format_list(list), channel, outputs)
    elif param == "players":
        list_players(argv, channel)
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
        return True
    else:
        return False

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
    plugin.reply("Selected %s" % movie.title, channel, outputs)

def shuffle_shows(show, channel):
    episode = random.choice(show.episodes())
    plugin.reply("Selected %s \"%s\"" % (show.title, episode.title), channel, outputs)
    return episode

def refresh(argv, channel):
    if len(argv) < 3:
        plugin.reply("Usage: plexcmd shuffle <library or show name>", channel, outputs)
        return None
    for library in plex.library.sections():
        if argv[2] == library.title:
            library.refresh()
            plugin.reply("Refreshing %s..." % library.title, channel, outputs)
            return library
    plugin.reply("Error: library %s not found (could not refresh)" % argv[2], channel, outputs)
    return library

def shuffle(argv, channel):
    liblist = get_libraries_list()
    if len(argv) < 3:
        plugin.reply("Usage: plexcmd shuffle <library or show name>", channel, outputs)
        return

    target = argv[2]
    if target in liblist:
        seclist = get_section_list(target)
        section = plex.library.section(target)
        random_item = plex.library.get(random.choice(seclist))
        if section.TYPE == 'movie':
            shuffle_movies(random_item, channel)
        elif section.TYPE == 'show':
            random_item = shuffle_shows(random_item, channel)
        if(play(random_item, channel)):
            plugin.reply("Playing on %s" % (player.name), channel, outputs)
        else:
            plugin.reply("Error: player disconnected or not set", channel, outputs)
    return

def process_message(data):
    try:
        channel = data["channel"]
        text = data["text"]

        #DM only
        if channel.startswith("D"):
            if text.lower().startswith("plex"):
                argv = shlex.split(text)
                if len(argv) < 2:
                    plugin.reply("plex <list> <setplayer> <shuffle> <refresh>", channel, outputs)

                options = {"list" : list,
                           "setplayer" : setplayer,
                           "shuffle" : shuffle,
                           "refresh" : refresh,
                }
                options[argv[1]](argv, channel)

    except Exception, error:
        print "%s: %s" % (error.__doc__, error.name)
        traceback.print_exec()
    return None



