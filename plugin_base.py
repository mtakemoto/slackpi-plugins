import re

class Plugin(object):
    
    def reply_all(self, message, channels, outputs):
        for channel in channels:
            print "sending %s to %s" % (message, channel)
            outputs.append([channel, message])
        return None

    def reply(self, message, channel, outputs):
        outputs.append([channel, message])
        print outputs
        return None

    def find_mentions(self, string):
        return re.findall(r'<@(.*?)>', string)

    def remove_mentions(self, string):
        return re.sub(r'<@(.*?)>', '', string)

    def parse_message(self, data):
        text = None
        if 'username' in data and data['username'] == 'IFTTT':
            a1 = data['attachments'][0]
            text = a1['pretext']
        else:
            if 'text' in data:
                text = data['text']
        return text

