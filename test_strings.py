ifttt = {u'username': u'IFTTT', u'attachments': [{u'pretext': u'plexcmd shuffle Movies -p default', u'fallback': u'plexcmd shuffle Movies -p default', u'mrkdwn_in': [u'text', u'pretext']}], u'icons': {u'image_36': u'https://slack.global.ssl.fastly.net/66f9/img/services/ifttt_36.png', u'image_48': u'https://slack.global.ssl.fastly.net/66f9/img/services/ifttt_48.png', u'image_72': u'https://slack.global.ssl.fastly.net/66f9/img/services/ifttt_72.png'}, u'ts': u'1451183245.000019', u'subtype': u'bot_message', u'mrkdwn': True, u'type': u'message', u'channel': u'C0HBP2MJL'}
bot_mentions = {u'text': u'multiple mention test <@U0GPPHAKT> <@USLACKBOT>', u'ts': u'1451186631.000022', u'user': u'U0GPPV0TG', u'team': u'T0GPPPLFR', u'type': u'message', u'channel': u'C0HBP2MJL'}
set_debug_dm = {u'text': u'!set debug off', u'ts': u'1451258588.000011', u'user': u'U0GPPV0TG', u'team': u'T0GPPPLFR', u'type': u'message', u'channel': u'D0GPM11DZ'}
plex = {u'text': u'plex', u'ts': u'1451258588.000011', u'user': u'U0GPPV0TG', u'team': u'T0GPPPLFR', u'type': u'message', u'channel': u'D0GPM11DZ'}
plex_shuffle = {u'text': u'plex shuffle Shows', u'ts': u'1451258588.000011', u'user': u'U0GPPV0TG', u'team': u'T0GPPPLFR', u'type': u'message', u'channel': u'D0GPM11DZ'}
set_debug_public = {u'text': u'!set debug off', u'ts': u'1451258588.000011', u'user': u'U0GPPV0TG', u'team': u'T0GPPPLFR', u'type': u'message', u'channel': u'D0GPM11DZ'}

strlist = ['ifttt', 'bot_mentions', 'set_debug_dm', 'set_debug_public']

def list_strings():
    for string in strlist:
        print string
        
def testall():
    process_message(plex); 

if __name__ == "__main__":
    from plexcmd import *
    testall()
