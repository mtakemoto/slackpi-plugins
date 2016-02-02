from plexapi.server import PlexServer
from plexapi.client import Client
from slackpi_base import SlackPi 
import random
import traceback
import time

outputs = []

class PlexCMD(SlackPi):
    def __init__(self):
        retries = 0
        while retries < 5:
            try:
                self.plex = PlexServer('http://localhost:32400')
                self.player = Client(self.plex, self.plex.query('/clients'))
                break
            except Exception:
                print "Error: server not found.  Retrying..."
                retries += 1
            time.sleep(5)

    def format_list(self, list):
        return ''.join(list)

    def listall(self, argv, channel):
        list = []
        param = argv[2]
        if param in self.get_libraries_list():
            for show in self.plex.library.section(param).all():
                list.append(show.title + '\n')
            SlackPi.reply(self, self.format_list(list), channel, outputs)
        elif param == "players":
            self.list_players(argv, channel)
        return None

    def list_players(self, argv, channel):
        clients = self.plex.clients()
        if not clients:
            SlackPi.reply(self, "no players connected", channel, outputs)
            return None
        for idx, client in enumerate(self.plex.clients()):
            response = "[%i] %s \n" % ((idx + 1), client.name)
            SlackPi.reply(self, response, channel, outputs)

    def setplayer(self, argv, channel):
        clients = self.plex.clients()
        if len(argv) > 2 and argv[2].isdigit() and int(argv[2]) <= len(self.plex.clients()):
            if clients:
                clinum = int(argv[2])
                self.player = self.plex.clients()[clinum - 1] 
                SlackPi.reply(self, "Player set to %s" % self.player.name, channel, outputs)
            else:
                SlackPi.reply(self, "Error: no clients", channel, outputs)
        else:
            SlackPi.reply(self, "Usage: plexcmd setplayer <player ID>", channel, outputs)
        return None

    def play(self, media, channel):
        if self.player.name:
            self.player.playMedia(media)
            return True
        else:
            return False

    def get_section_list(self, secname):
        list = []
        for item in self.plex.library.section(secname).all():
            list.append(item.title)
        return list

    def get_libraries_list(self):
        libs = []
        for section in self.plex.library.sections():
            libs.append(section.title)
        return libs

    def shuffle_movies(self, movie, channel):
        SlackPi.reply(self, "Selected %s" % movie.title, channel, outputs)

    def shuffle_shows(self, show, channel):
        episode = random.choice(show.episodes())
        SlackPi.reply(self, "Selected %s \"%s\"" % (show.title, episode.title), channel, outputs)
        return episode

    def refresh(self, argv, channel):
        if len(argv) < 3:
            SlackPi.reply(self, "Usage: plexcmd shuffle <library or show name>", channel, outputs)
            return None
        for library in self.plex.library.sections():
            if argv[2] == library.title:
                library.refresh()
                SlackPi.reply(self, "Refreshing %s..." % library.title, channel, outputs)
                return library
        SlackPi.reply(self, "Error: library %s not found (could not refresh)" % argv[2], channel, outputs)
        return library

    def shuffle(self, argv, channel):
        liblist = self.get_libraries_list()
        if len(argv) < 3:
            SlackPi.reply(self, "Usage: plexcmd shuffle <library or show name>", channel, outputs)
            return
        target = argv[2]
        if target in liblist:
            seclist = self.get_section_list(target)
            section = self.plex.library.section(target)
            random_item = self.plex.library.get(random.choice(seclist))
            if section.TYPE == 'movie':
                self.shuffle_movies(random_item, channel)
            elif section.TYPE == 'show':
                random_item = self.shuffle_shows(random_item, channel)
            if(self.play(random_item, channel)):
                SlackPi.reply(self, "Playing on %s" % (self.player.name), channel, outputs)
            else:
                SlackPi.reply(self, "Error: player disconnected or not set", channel, outputs)
        return

