#Settings Plugin
from slackpi_base import SlackPi 

outputs = []

class Settings(SlackPi):
    debug_mode = False

    def debug(argv, channel):
        if(argv[2] == 'on'):
            debug_mode = True
            SlackPi.reply("Debug on", channel, outputs)
        elif(argv[2] == 'off'):
            debug_mode = False
            SlackPi.reply("Debug off", channel, outputs)
        else:
            print "invalid argument for debug"


def process_message(data):
    try:
        text = parse_message(data)
        channel = data["channel"]
        mention_list = []
        print data
        #initially set the reply to the message channel like in a PM
        reply_to = channel

        #if posted in a public channel, message tagged users privately
        if channel.startswith("C"):
            mention_list = find_mentions(text) 
            text = remove_mentions(text)
            reply_to = mention_list
        if "!set" in text:
            argv = text.split()

            options = {"debug" : debug}
            options[argv[1]](argv, reply_to)
    except Exception, error:
        print str(error)

    return
