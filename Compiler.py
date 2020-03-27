# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 03:14:42 2020

@author: vjspranav
"""
import logging

import telegram
import subprocess
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_CODE_C, GET_INP_C, GET_CODE_CPP, GET_INP_CPP = range(4)

TOKEN='Your Token Here'
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I'll help you compile all your codes trust me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def c2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK give me some c code to execute")
    return GET_CODE_C


def get_code_c(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="entered this function ")
    c_code = update.message.text
    f=open("test.c","w+")
    f.write(c_code)
    f.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter inputs(if any) or send 0 ")
    return GET_INP_C    
    
def get_inp_c(update, context):
    inp = update.message.text
    f=open("input.txt","w+")
    f.write(inp)
    f.close()    
    if(subprocess.call("gcc test.c -o test.exe", shell="True") ==0 ):
        subprocess.call("test.exe < input.txt > temp.txt", shell="True")
        y=''
        f=open("temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen(['gcc', "test.c", '-o', 'test.exe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("test.c", "Code")
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END
    
def cpp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK give me some c++ code to execute")
    return GET_CODE_CPP


def get_code_cpp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="entered this function ")
    cpp_code = update.message.text
    f=open("test.cpp","w+")
    f.write(cpp_code)
    f.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter inputs(if any) or send 0 ")
    return GET_INP_CPP    
    
def get_inp_cpp(update, context):
    inp = update.message.text
    f=open("input.txt","w+")
    f.write(inp)
    f.close()    
    if(subprocess.call("g++ test.cpp -o test.exe", shell="True") ==0 ):
        subprocess.call("test.exe < input.txt > temp.txt", shell="True")
        y=''
        f=open("temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen(['g++', "test.cpp", '-o', 'test.exe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("test.cpp", "Code")
        context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END
    
def done():
    pass    


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('c', c2), CommandHandler('cpp', cpp)],

        states={
            GET_CODE_C: [MessageHandler(Filters.text, get_code_c)],
            GET_INP_C: [MessageHandler(Filters.text, get_inp_c)],    
            GET_CODE_CPP: [MessageHandler(Filters.text, get_code_cpp)],
            GET_INP_CPP: [MessageHandler(Filters.text, get_inp_cpp)],    
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
