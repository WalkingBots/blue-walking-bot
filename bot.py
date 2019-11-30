# создаем телеграм бота
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.utils.request import Request

import config
import dump

req = Request(proxy_url=config.proxy)
bot = Bot(config.token, request=req)
upd = Updater(bot=bot, use_context=True)
dp = upd.dispatcher

data = dict()

# логирование
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# приветственное сообщение
def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Приветствую! Я бот урбанист {0}. Для того, чтобы дополнить нашу карту информацией, пришилите нам запись звука.".format(config.name))

ASK_PEAKS, ASK_SOURCE, ASK_LOCATION = 0, 1, 2

def voice(update, context):
    data[update.message.from_user.username] = [bot.get_file(update.message.voice.file_id), None, None, None]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Отправьте мне мощность звука в peaks")
    return ASK_PEAKS

def peaks(update, context):
    if not update.message.text.isnumeric():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вы ввели не число")
        return ASK_PEAKS
    else:
        if int(update.message.text) > 150:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Слишком высокое значение")
            return ASK_PEAKS
        else:
            data[update.message.from_user.username][1] = update.message.text
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Отправьте мне название источника звука")
            return ASK_SOURCE


def source(update, context):
    data[update.message.from_user.username][2] = update.message.text
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    custom_keyboard = [[location_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.effective_chat.id,
                    text="Пришли мне пожалуйста, свое местоположение :)",
                    reply_markup=reply_markup)

    return ASK_LOCATION

def location(update, context):
    un = update.message.from_user.username
    data[un][3] = update.message.location
    dump.voice_source_peaks_location(*data[un], un)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Благодорим за отправленную информацию")

    return ConversationHandler.END

dp.add_handler(CommandHandler('start', hello))

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Спасибо за внимание!")

dp.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.voice, voice)],

    states={
        ASK_PEAKS: [MessageHandler(Filters.text, peaks)],

        ASK_SOURCE: [MessageHandler(Filters.text, source)],

        ASK_LOCATION: [MessageHandler(Filters.location, location)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
))

def main():
    # запускаем бота
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()
