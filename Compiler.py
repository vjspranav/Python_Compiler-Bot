# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 18:57:28 2020

@author: vjspranav
"""

import telegram
import subprocess
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

TOKEN='Your Token ID here'
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I'll help you compile all your codes trust me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def c(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    c_code = update.message.text[2:]
    f=open("R:/test.c","w+")
    f.write(c_code)
    f.close()
    if(subprocess.call("gcc R:/test.c -o R:/test.exe", shell="True") ==0 ):
        subprocess.call("R:/test.exe > R:/temp.txt", shell="True")
        y=''
        f=open("R:/temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen(['gcc', "R:/test.c", '-o', 'R:/test.exe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("R:/test.c", "Code")
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)

c_handler = CommandHandler("c", c)
dispatcher.add_handler(c_handler) 
    
    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



