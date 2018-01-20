from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def judgeHandler(bot, update):
    update.message.reply_text(update.message.text +' Judge')

def botHandler(bot, update):
    user = update.message.from_user
    if(user.is_bot):
        update.message.reply_text(update.message.text +' Bot')
    else:
        update.message.reply_text("CHEATER")

def main():

    tokenFile = open('Token', 'r')
    TOKEN = tokenFile.read(45);
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.group, botHandler))
    dp.add_handler(MessageHandler(Filters.text, judgeHandler))


    updater.start_polling()
    print("bot started.")

    updater.idle()


if __name__ == '__main__':
    main()
