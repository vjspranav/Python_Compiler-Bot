# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 03:14:42 2020

@author: vjspranav
"""
import logging
import os
import telegram
import subprocess
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_CODE_C, GET_INP_C, GET_CODE_CPP, GET_INP_CPP, GET_IPY, GET_CODE_PY, GET_INP_PY, GET_CODE_JAVA, GET_INP_JAVA, GET_DEN = range(10)

TOKEN=os.environ['TOKEN']
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
updater = Updater(token=TOKEN, use_context=True)
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I'll help you compile all your codes trust me!\PS: I take care of sepolicy denials too\n/c - For C\n/cpp - For C++\n/ipy - For Interpretter\n/py - For Python\n/denial - For Denials")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def c2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK give me some c code to execute")
    return GET_CODE_C


def get_code_c(update, context):
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
    if(subprocess.call("gcc test.c -o test", shell="True") ==0 ):
        subprocess.call("./test < input.txt > temp.txt", shell="True")
        y=''
        f=open("temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen(['gcc', "test.c", '-o', 'test.exe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("test.c", "Code")
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END

def cpp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK give me some c++ code to execute")
    return GET_CODE_CPP


def get_code_cpp(update, context):
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
    if(subprocess.call("g++ test.cpp -o test", shell="True") ==0 ):
        subprocess.call("./test < input.txt > temp.txt", shell="True")
        y=''
        f=open("temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen(['g++', "test.cpp", '-o', 'test'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("test.cpp", "Code")
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END

def ipy(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Python interpretter, please enter exit() to stop\nAs of now Inputs are not supported do exit() and use /py for input supported code and at any point if it feels unresponsive due to any unresponsive code please exit and restart.")
    f=open("temp.txt","w")
    f.close()
    return GET_IPY

def get_ipy(update, context):
    py_code = update.message.text
    if 'exit()' in py_code:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for using.")
        os.remove('temp.txt')
        os.remove("test.py")
        return ConversationHandler.END

    f=open("test.py","a+")
    f.write(py_code+'\n')
    f.close()
    f=open("temp.txt","r")
    lenf=len(f.read())
    f.close()
    subprocess.call("python3 test.py > temp.txt", shell="True")
    y=''
    f=open("temp.txt","r")
    for i in f.readlines():
        y = y + str(i)
    f.close()
    if y:
        context.bot.send_message(chat_id=update.effective_chat.id, text=y[lenf:])
    return GET_IPY

def py(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK give me some python code to execute")
    return GET_CODE_PY


def get_code_py(update, context):
    py_code = update.message.text
    f=open("test.py","w+")
    f.write(py_code)
    f.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter inputs(if any) or send 0 ")
    return GET_INP_PY    
    
def get_inp_py(update, context):
    inp = update.message.text
    f=open("input.txt","w+")
    f.write(inp)
    f.close()    
    if(subprocess.call("python test.py < input.txt > temp.txt", shell="True") ==0 ):
        y=''
        f=open("temp.txt","r")
        for i in f.readlines():
            y = y + str(i)
        f.close()
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    else:
        process = subprocess.Popen('python test.py < input.txt > temp.txt', stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (x, _) = process.communicate()
        x = x.decode("utf-8")
        y = "There were some errors\n"
        y = y + x
        y = y.replace("test.py", "Code")
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END

def java(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="The Java part is still under work")
    return GET_CODE_JAVA

def get_code_java(update, context):
    java_code = update.message.text
    f=open("Test.java","w+")
    f.write(c_code)
    f.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter inputs(if any) or send 0 ")
    return GET_INP_JAVA

def get_inp_java(update, context):
    inp = update.message.text
    f=open("input.txt","w+")
    f.write(inp)
    f.close()
#    if(subprocess.call("javac test.java", shell="True") ==0 ):
    subprocess.call("javac Test.java", shell="True")
    subprocess.call("java Test > temp.txt", shell="True")
    y=''
    f=open("temp.txt","r")
    for i in f.readlines():
        y = y + str(i)
        f.close()
        if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
#    else:
#        process = subprocess.Popen(['gcc', "test.c", '-o', 'test.exe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
#        (x, _) = process.communicate()
#        x = x.decode("utf-8")
#        y = "There were some errors\n"
#        y = y + x
#        y = y.replace("test.c", "Code")
#        if y:
#            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END

def denial(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a log(either file or the denials or the denial line): ")
    return GET_DEN
    
def get_den(update, context):
    res = []
    lines = []
    try:
        user_command=update.message.text
    except AttributeError:
        user_command=None
        pass

    if not user_command:
        try:
            newfile=update.message.document
            bot.send_message(chat_id=update.effective_chat.id, text="Downloading file %s (%i bytes)" %(newfile.file_name, newfile.file_size))
            newFile = bot.getFile(newfile.file_id)
            link=open(newFile.download(newfile.file_name))
            link = link.readlines()
            for i in link:
                if 'avc:' in i:
                    lines.append(i)
        except AttributeError:
            pass
    else:
        for i in user_command.split('\n'):
            if 'avc:' in i:
                lines.append(i)

    y = ''
    c=0
    
    for a in lines:
        perm = [x for x in a.split(" ")]
        for i in range(len(perm)):
            if(perm[i] == '{'):
                per = perm[i+1]
            if('scontext=' in perm[i]):
                scon = (perm[i].split('u:r:')[1]).split(':s0')[0]
            if('tcontext=' and 'u:object_r:' in perm[i]):
                tcon = perm[i].split('u:object_r:')[1].split(':s0')[0]
            if('tcontext=' and 'u:r:' in perm[i]):
                tcon = perm[i].split('u:r:')[1].split(':s0')[0]
            if('tclass=' in perm[i]):
                tcl = perm[i].split('tclass=')[1]
        b = "allow " + scon + " " + tcon + ":" + tcl + " { " + per + " };"
        if b not in res: #Checking if denial resolution already exists or not
            res.append(b) #Adds the resolution to list
    res.sort()    
    #Adding multiple permissions to same line
    for i in range(1,len(res)):
        c=i
        while(res[c].split(' ')[2]==res[i-1].split(' ')[2] and res[c].split(' ')[1]==res[i-1].split(' ')[1]):
            res[i-1] = res[i-1][:-2] + ' ' + res[c].split(' ')[4] + ' ' + res[0][-2:]
            res[c]='0 0 0 0 0'
            c += 1
            if(c==len(res)):
                break
        i=c
    
    res = [ i for i in res if '0 0 0 0' not in i]
    for i in res:
        y = y+ "in " + i.split(' ')[1]+".te\n"+i+"\n\n"
        print(y)

    if y:
            context.bot.send_message(chat_id=update.effective_chat.id, text=y)
    return ConversationHandler.END

def done():
    pass

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('c', c2), CommandHandler('cpp', cpp), CommandHandler('ipy', ipy), CommandHandler('py', py), CommandHandler('java', java), CommandHandler('denial', denial)],

            states={
                GET_CODE_C: [MessageHandler(Filters.text, get_code_c)],
                GET_INP_C: [MessageHandler(Filters.text, get_inp_c)],
                GET_CODE_CPP: [MessageHandler(Filters.text, get_code_cpp)],
                GET_INP_CPP: [MessageHandler(Filters.text, get_inp_cpp)],
                GET_IPY:  [MessageHandler(Filters.text, get_ipy)],
                GET_CODE_PY: [MessageHandler(Filters.text, get_code_py)],
                GET_INP_PY: [MessageHandler(Filters.text, get_inp_py)],
                GET_CODE_JAVA: [MessageHandler(Filters.text, get_inp_java)],
                GET_INP_JAVA: [MessageHandler(Filters.text, get_inp_java)],
                GET_DEN: [MessageHandler(Filters.text | Filters.document, get_den)],
            },

            fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
        )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
