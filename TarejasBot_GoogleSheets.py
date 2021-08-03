"""
The intention of this program is to provide an easy way for me and my girlfriend, Mikaela, to have a to-do list of items to keep track of and help to increase our productivity. I've made my best attempt to add comments along the code to explain what's going on however if it's still difficult to follow there are additional tutorials linked in the documentation

I've added Google Sheets functionality to this which will make it easier if the server running the bot shuts down etc
"""
import datetime, os #adds functionality for printing the date
from telegram.ext import Updater, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
os.environ['TZ'] = 'America/New_York' #makes the program recognize the current timezone as mine
updater = Updater(token = 'TELEGRAM_TOKEN')
dispatcher = updater.dispatcher
# INITIALIZE THE GOOGLE SHEET USING GSPREAD
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
gc = gspread.authorize(credentials)
tarejas = gc.open('TarejasBot').sheet1

# Chat ID is used for authorization to use the bot, let's retrieve it from the text file
chat_ID = open("chat_ID.txt", "r")

for line in chat_ID:
    line = line.strip()
    chat_ID = int(line)

jordan_tasks = []
mikaela_tasks = []


# Does an authorization check to see if the message is from the correct chat
def check_chat(bot, update):
    #print (type(update.message.chat_id))
    #print (type(chat_ID))
    #check_ID = update.message.chat_id
    #print (chat_ID)
    #print (update.message.chat_id)
    #check_ID = check_ID.strip()
    #print (check_ID)
    #print (chat_ID == update.message.chat_id)
    if (update.message.chat_id != chat_ID):
        bot.send_message(chat_id=update.message.chat_id, text="YOU ARE IN VIOLATION AND THIS OFFENSE HAS BEEN REPORTED. EXIT CHAT NOW!")
        bot.send_message(chat_id=chat_ID, text = "Unauthorized user has accessed bot")
        return "error"

def retrieveValues(array, column, start_value):
    """retrieve the data from specified column in Sheets and store in array"""
    i = start_value
    cellValue = 'initialize'
    while (cellValue != ''):
        cellValue = tarejas.acell('%s%d' % (column, i)).value
        #cellValue = '- ' + cellValue
        if '-' not in cellValue:
            arrVal = '- ' + cellValue
        else:
            arrVal = cellValue
        array.append(arrVal)
        i += 1
    del array[-1]


retrieveValues(jordan_tasks, 'A', 2)
retrieveValues(mikaela_tasks, 'B', 2)


def updateSheets(array, column, start_value):
    i = start_value
    x = i
    cellValue = 'initialize'
    while (cellValue != ''):
        cellValue = tarejas.acell('%s%d' % (column, x)).value
        tarejas.update_acell('%s%d' % (column, x), '')
        x += 1
    for item in array:
        tarejas.update_acell('%s%d' % (column, i), item)
        i += 1

def printTasks(): # this function constructs the task format and returns a variable the bot can use to print to the users all the tasks to be done
    today = datetime.date.today()
    dateList = []
    dateList.append(today)
    taskPrint = "LIST OF TASKS TO-DO FOR "+str(dateList[0]) #the date is put in a string format for it to be used with the other strings easily
    taskPrint += '\n\nJordan: '
    for i in range(len(jordan_tasks)): #runs a loop to gather all the items in the working list
        taskPrint += '\n'
        taskPrint += (jordan_tasks[i] + ' ('+str(i+1) + ')') #this adds in brackets the number of the task in the list
    taskPrint += '\n\nMikaela: '
    for i in range(len(mikaela_tasks)):
        taskPrint += '\n'
        taskPrint += (mikaela_tasks[i]+ ' ('+str(i+1) + ')') #this adds in brackets the number of the task in the list
    return taskPrint


def tasks(bot, update, args): #function declaration. takes the bot and update objects as well as the arguments passed with the command
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    if args[0] == 'Jordan' or args[0] == 'jordan':
        args.pop(0) #remove the first argument as it would not be used past knowing what list of tasks to put it in
        args.insert(0,'-')
        args = ' '.join(args) #converts the list of arguments into a single string
        jordan_tasks.append(args)    #adds the arguments (minus the name of the individual) to the list of tasks
    if args[0] == 'Mikaela' or args[0] == 'mikaela':
        args.pop(0)
        args.insert(0,'-')
        args = ' '.join(args)
        mikaela_tasks.append(args)
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat


def clear(bot, update): # purpose of this function is to clear the lists
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    del jordan_tasks[:]
    del mikaela_tasks[:]
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text='Task lists cleared :)')
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat


def remove(bot, update, args): #allows the user to erase individual lines
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    index = int(args[1]) #passes the second argument to the variable
    index-=1 #users use standard ordinal numbers this converts it to the index form
    if args[0] == 'Jordan' or args[0] == 'jordan':
        jordan_tasks.pop(index) #removes the item in the list at that index number
    if args[0] == 'Mikaela' or args[0] == 'mikaela':
        mikaela_tasks.pop(index)
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text='Task cleared :)')
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat


def check_task(bot, update, args):
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    index = int(args[1]) #this is the second argument passed to the bot in the command that we're turning into an integer
    index -= 1    #the integer is decremented as the user would not use the index value but the regular numbered value of the item in the list
    if args[0] == 'Jordan' or args[0] == 'jordan':
        jordan_tasks[index] += u' \u2714'        #adds the unicode tick to the list item
    if args[0] == 'Mikaela' or args[0] == 'mikaela':
        mikaela_tasks[index] += u' \u2714'
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text='checked :)')
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint)

def bulkadd(bot,update,args):
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    user = args[0]
    args.pop(0)
    args = " ".join(args)        #join all elements, turning it into one big string
    args = [s.strip() for s in args.split(',')]        #splits it at the comma and removes the spaces
    for argument in args:
        argument = '- ' + argument
        if user == 'Jordan' or user == 'jordan':
            jordan_tasks.append(argument)
        if user == 'Mikaela' or user == 'mikaela':
            mikaela_tasks.append(argument)
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint)

def bulkcheck(bot, update, args):
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    user = args[0]
    args.pop(0)        #removes the name of the user from the list
    for argument in args:
        index = int(argument) - 1
        if user == 'Jordan' or user == 'jordan':
            jordan_tasks[index] += u' \u2714'
        if user == 'Mikaela' or user == 'mikaela':
            mikaela_tasks[index] += u' \u2714'
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text='all tasks checked :)')
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint)

def bulkremove(bot, update, args):
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    user = args[0]
    user = user.lower()
    args.pop(0)
    global jordan_tasks
    global mikaela_tasks
    for argument in args:
        index = int(argument) - 1
        if user == "jordan":
            jordan_tasks[index] = "BLANK"
        if user == "mikaela":
            mikaela_tasks[index] = "BLANK"
    #comprehensive list removal of all strings that are equal to "BLANK"
    jordan_tasks = [s for s in jordan_tasks if s!= "BLANK"]
    mikaela_tasks = [s for s in mikaela_tasks if s!= "BLANK"]
    taskPrint = printTasks()
    bot.send_message(chat_id=update.message.chat_id, text='tasks cleared x)')
    bot.send_message(chat_id=update.message.chat_id, text=taskPrint)

def saveInfo(bot, update):
    check_result = check_chat(bot,update)
    if check_result == "error":
        return
    bot.send_message(chat_id=update.message.chat_id, text='hold tight')
    updateSheets(jordan_tasks,'A',2)
    updateSheets(mikaela_tasks,'B',2)
    bot.send_message(chat_id=update.message.chat_id, text='tasks saved!')



task_handler = CommandHandler('newtask',tasks,pass_args = True) #creates a new command handler that allows arguments to be passed with the telegram command, arguments are considered all strings after the initial command
check_handler = CommandHandler('check',check_task,pass_args = True)
clear_handler = CommandHandler('clear',clear)
remove_handler = CommandHandler('remove',remove, pass_args = True)
batch_task_handler = CommandHandler('bulkadd', bulkadd, pass_args = True)
batch_task_check_handler = CommandHandler('bulkcheck', bulkcheck, pass_args = True)
batch_remove_handler = CommandHandler('bulkremove', bulkremove, pass_args = True)
save_sheets_handler = CommandHandler('save', saveInfo)
dispatcher.add_handler(task_handler) #adds the newly created handler to the dispatcher. this allows it to be used in the running of the bot
dispatcher.add_handler(check_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(remove_handler)
dispatcher.add_handler(batch_task_handler)
dispatcher.add_handler(batch_task_check_handler)
dispatcher.add_handler(batch_remove_handler)
dispatcher.add_handler(save_sheets_handler)
updater.start_polling() #updater starts polling messages and input from the user(s) in the chat
