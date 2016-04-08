import urllib2, urllib, json
import datetime
from ConfigParser import SafeConfigParser

'''Query OpenWeatherMap API for data
Free Options:
    Current Weather
    5 Day Forecast
    Maps API
'''

parser = SafeConfigParser()
parser.read("plugins/config.ini")

class Weather(object):
    def __init__(self, zip):
        self.baseurl = "http://api.openweathermap.org/data/2.5/"
        self.zipcode = zip
        self.apikey = parser.get('apikeys', 'openweather')
        self.units = "imperial"
        self.currentdata = None
        self.forecastdata = None
        self.lastRequest = None

    def set_units(self, input):
        if(input == "f"):
            self.units = "imperial"
        elif(input == "c"):
            self.units = "metric"
        elif(input == "k"):
            self.units = ""

    #Check last query time & run only if >1 min elapsed
    def get_current(self):
        type = "weather?"
        zipcode = "zip=" + self.zipcode + ",us"
        apikey = "&appid=" + self.apikey
        units = "&units=" + self.units
        query_str = self.baseurl + type + zipcode + apikey + units

        print query_str
        result = urllib2.urlopen(query_str).read()
        self.currentdata = json.loads(result)
        print self.currentdata

    def get_temp(self, do_round=False):
        if not(do_round):
            return str(self.currentdata['main']['temp'])
        else:
            val = int(round(self.currentdata['main']['temp']))
            return str(val)

    def get_humidity(self):
        return str(self.currentdata['main']['humidity'])

    def get_main_status(self):
        return str(self.currentdata['weather'][0]['main'])

    def get_description(self):
        return str(self.currentdata['weather'][0]['description'])

    def get_wind(self):
        return str(round(self.currentdata['wind']['speed'], 1))

    #User Facing Functions
    #must take argv and a slack channel just in case
    def report_basic(self, argv=None):
        #Reload data. Need to add over-limit handling or rate limiting
        self.get_current()

        temp = self.get_temp(True) + " deg"
        status = ", " + self.get_main_status()
        wind = " " + self.get_wind() + " MPH"
        text = temp + status + wind
        print text
        return text

    def report(self, argv=None):
        #Reload data. Need to add over-limit handling or rate limiting
        self.get_current()

        temp = self.get_temp() + " degrees"
        status = ", " + self.get_description()
        wind = ", " + self.get_wind() + " MPH"
        text = temp + status + wind
        timestamp = self.currentdata['dt']
        time = datetime.datetime.fromtimestamp(timestamp).strftime("%B %d, %Y at %I:%M:%S %p")
        text += "\nGenerated on " + time
        print text
        return text
