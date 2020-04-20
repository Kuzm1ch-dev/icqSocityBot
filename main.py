#Чисто поржать сделал, не судите строго

from bot.bot import Bot
from bot.filter import Filter, InvertFilter
from bot.handler import HelpCommandHandler, UnknownCommandHandler, MessageHandler, FeedbackCommandHandler, \
    CommandHandler, NewChatMembersHandler, LeftChatMembersHandler, PinnedMessageHandler, UnPinnedMessageHandler, \
    EditedMessageHandler, DeletedMessageHandler, StartCommandHandler, BotButtonCommandHandler

TOKEN = ""

looking = list()
interlocutors = dict()

bot = Bot(token=TOKEN, api_url_base="https://api.icq.net/bot/v1")

def FindInterlocutor(item):
    for key in interlocutors:
        if key == item:
            return(interlocutors.get(key))
        if interlocutors.get(key) == item:
            return(key)
    return(None)

def DelInterlocutor(item):
    for key in interlocutors:
        if key == item:
            return(interlocutors.pop(item))
        if interlocutors.get(key) == item:
            return(interlocutors.pop(key))
    return(None)


def Newinterlocutor(item):
    bot.send_text(chat_id=FindInterlocutor(item), text="Ваш собеседник покинул чат, пишите /find, чтобы найти нового!")

def find(userId):
    if userId in looking:
        if len(looking) > 1:
            looking.remove(userId)
            if userId != looking[0]:
                bot.send_text(chat_id=userId, text="Мы нашли вам собеседника!")
                bot.send_text(chat_id=looking[0], text="Мы нашли вам собеседника!")
                interlocutors.update({userId : looking[0]})
                looking.remove(looking[0])
                looking.remove(userId)
            else:
                bot.send_text(chat_id=userId, text="Пока никто не ищет собеседника, ожидаем!")
        else:
            bot.send_text(chat_id=userId, text="Пока никто не ищет собеседника, ожидаем!")

def AddIntoQueue(userId):
    looking.append(userId)
    bot.send_text(chat_id=userId, text="Вы стали в очередь, мы ищим вам собеседника!")
    find(userId)

def start_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Привет, я бот призванный найти тебе друзей! Пишите /find, когда пожелаете начать и я найду вам собеседника.")

def help_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Пиши /find, чтобы найти собеседника")

def startchat_cb(bot, event):
    userId = event.data['from']['userId']
    if FindInterlocutor(userId) is not None:
        Newinterlocutor(userId)
        AddIntoQueue(userId)
        return
    if userId not in looking:
        AddIntoQueue(userId)
        return

def new_chat_message_cb(bot, event):
    interlocutor = FindInterlocutor(event.data['from']['userId'])
    if interlocutor is not None:
        bot.send_text(chat_id=interlocutor, text=event.text)
    else:
        if event.data['from']['userId'] in looking:
            bot.send_text(chat_id=event.data['from']['userId'], text="Мы сообщим вам, когда найдем собеседника!")
        else:
            bot.send_text(chat_id=event.data['from']['userId'], text="Пиши /find ,чтобы найти собеседника")

def main():
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
    bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))
    bot.dispatcher.add_handler(CommandHandler(command="find", callback=startchat_cb))
    bot.dispatcher.add_handler(MessageHandler(filters = InvertFilter(Filter.command), callback=new_chat_message_cb))


if __name__ == "__main__":
    main()


bot.start_polling()
bot.idle()