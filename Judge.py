from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from collections import deque

judge_queue = deque()
chat_dictionary = dict()
score_dictionary = dict()


def start(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat.id
    if update.message.chat.type == 'group':
        bot.send_message(chat_id, "Hi bot")
        if len(judge_queue) == 0:
            bot.send_message(chat_id, "No")
        else:
            judge = judge_queue.popleft()
            chat_dictionary[judge[0]] = ((chat_id, user), judge[1])
            chat_dictionary[chat_id] = (judge, user)
            bot.send_message(judge[0], "Judge you are now talking to a bot, or not :D")
            bot.send_message(chat_id, "You are now talking to the judge, good luck")
    else:
        bot.send_message(chat_id, "Hi Judge")
        judge_queue.append((chat_id, user))


def judge_handler(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat.id
    print(update.message.chat.type)
    if chat_id in chat_dictionary:
        bot.send_message(chat_dictionary[chat_id][0][0], update.message.text)
    else:
        bot.send_message(chat_id,
                         "Sorry, no one is listening to what you're saying, use /start to start a conversation")


def bot_handler(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat.id
    if not user.is_bot:
        if chat_id in chat_dictionary:
            bot.send_message(chat_dictionary[chat_id][0][0], update.message.text)
        else:
            if (chat_id, user) in score_dictionary:
                score_dictionary[(chat_id, user)] = (update.message.text, score_dictionary[(chat_id, user)][1])
                # TODO: mongoDB call
                bot.send_message(chat_id, 'امتیاز شما ثبت شد')
            else:
                bot.send_message(chat_id,
                                 'Sorry, no one is listening to what you\'re saying, use /start to start a conversation')
    else:
        update.message.reply_text("Don't cheat, let the bot do the talking")


def end(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat.id
    if not user.is_bot:
        judge = (chat_id, user)
        chat_bot = chat_dictionary[chat_id][0]
        del chat_dictionary[chat_id]
        del chat_dictionary[chat_bot[0]]
        score_dictionary[judge] = (-1, chat_bot)


def main():
    tokenFile = open('Token', 'r')
    TOKEN = tokenFile.read(45);
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("end", end))
    dp.add_handler(MessageHandler(Filters.group, bot_handler))
    dp.add_handler(MessageHandler(Filters.text, judge_handler))

    updater.start_polling()
    print("bot started.")

    updater.idle()


if __name__ == '__main__':
    main()
