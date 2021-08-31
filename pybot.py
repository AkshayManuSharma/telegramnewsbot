import logging
from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import get_reply, fetch_news

#enable logging
logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
@app.route('/')
def index():
    return "Hello!"
@app.route('/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "ok"



#enable updating
TOKEN = "1960055629:AAE9G1cFJNGN4gvPBgFGLd_NRBklQA31DQU"

def start (bot, update):
    print(update)
    author = update.message.from_user.first_name
    reply = "HI! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def help (bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Go help yourself")

def reply_text(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id )
    if(intent == "get_news"):
       articles = fetch_news(reply)
       for article in articles:
           bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot, update):
    reply = update.message.text
    bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot, update):
    logger.error("update '%s' caused an error'%s'", update, update.error)

def main():
        bot = Bot(TOKEN)
        bot.set_webhook("URL HERE" + TOKEN)
        dt = Dispatcher(bot, None)

        dt.add_handler(CommandHandler("start", start))
        dt.add_handler(CommandHandler("help", help))
        dt.add_handler(MessageHandler(Filters.sticker, echo_sticker))
        dt.add_handler(MessageHandler(Filters.text, reply_text))
        dt.add_error_handler(error)
        updater.start_polling()
        logger.info("Polling initiated...")
        updater.idle()

if (__name__ == "__main__"):
    main()