import time
import telepot
from telepot.loop import MessageLoop

from config import *


bot = telepot.Bot(TOKEN)

if PROXY:
    telepot.api.set_proxy(PROXY)


def msg_with_link(msg):
    link = "https://t.me/c/%s/%d" % (str(msg['chat']['id'])[4:], msg['message_id'])
    message = "Report: " + link
    return message


def handle(msg):
    print(msg)

    with open(LOG_FILE, 'a') as log:
        log.write(str(msg)+'\n')

    if msg.get('chat',{}).get('id') in CHATS_TO_MONITOR \
       and msg.get('text', '').startswith('/moderator'):
        bot.sendMessage(MODERATOR_CHAT, msg_with_link(msg))
        # forward original message
        if msg.get('reply_to_message'):
            bot.forwardMessage(MODERATOR_CHAT, msg['chat']['id'], msg['message_id'])


MessageLoop(bot, handle).run_as_thread()


while 1:
    time.sleep(10)
