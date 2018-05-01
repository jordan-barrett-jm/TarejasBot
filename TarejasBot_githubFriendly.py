"""A Telegram bot that is used for managing tasks throughout the day"""
import datetime #adds functionality for printing the date
import os
from telegram.ext import Updater, CommandHandler
os.environ['TZ'] = 'America/New_York' #makes the program recognize the current timezone as mine
UPDATER = Updater(token='[bot_token]')
DISPATCHER = UPDATER.dispatcher
USER1_TASKS = []
USER2_TASKS = []
def print_tasks():
    """Print the tasks stored in the task arrays"""
    #this function constructs the task format and
	#returns a variable the bot can use to print to the users all the tasks to be done
    today = datetime.date.today()
    date_list = []
    date_list.append(today)
    task_print = "LIST OF TASKS TO-DO FOR "+str(date_list[0])
	#the date is put in a string format for it to be used with the other strings easily
    task_print += '\n\nuser1: '
    for i in range(len(USER1_TASKS)):
		#runs a loop to gather all the items in the working list
        task_print += '\n'
        task_print += (USER1_TASKS[i] + ' ('+str(i+1) + ')')
		#this adds in brackets the number of the task in the list
    task_print += '\n\nuser2: '
    for i in range(len(USER2_TASKS)):
        task_print += '\n'
        task_print += (USER2_TASKS[i]+ ' ('+str(i+1) + ')')
		#this adds in brackets the number of the task in the list
    return task_print

def tasks(bot, update, args):
    """Add a new task to the task array for the specific user"""
    if args[0] == 'user1' or args[0] == 'user1':
        args.pop(0)
		#remove the first argument as it would not be used past knowing what list of tasks to put it in
        args.insert(0, '-')
        args = ' '.join(args)
		#converts the list of arguments into a single string
        USER1_TASKS.append(args)
		#adds the arguments (minus the name of the individual) to the list of tasks
    if args[0] == 'user2' or args[0] == 'user2':
        args.pop(0)
        args.insert(0, '-')
        args = ' '.join(args)
        USER2_TASKS.append(args)
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text=task_print)
	 #sends all the content in the task_print variable to the chat


def clear(bot, update):
	#purpose of this function is to clear the lists
    """"Clear the task stored for all users"""
    del USER1_TASKS[:]
    del USER2_TASKS[:]
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text='Task lists cleared :)')
    bot.send_message(chat_id=update.message.chat_id, text=task_print)
	#sends all the content in the task_print variable to the chat


def remove(bot, update, args): #allows the user to erase individual lines
    """Remove a specific task"""
    index = int(args[1]) #passes the second argument to the variable
    index -= 1 #users use standard ordinal numbers this converts it to the index form
    if args[0] == 'user1' or args[0] == 'user1':
        USER1_TASKS.pop(index) #removes the item in the list at that index number
    if args[0] == 'user2' or args[0] == 'user2':
        USER2_TASKS.pop(index)
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text='Task cleared :)')
    bot.send_message(chat_id=update.message.chat_id, text=task_print)
	#sends all the content in the task_print variable to the chat


def check_task(bot, update, args):
    """Put a check beside a task to indicate it has been done"""
    index = int(args[1])
	#this is the second argument passed to the bot in the command that we're turning into an integer
    index -= 1
	#the integer is decremented for user convenience
    if args[0] == 'user1' or args[0] == 'user1':
        USER1_TASKS[index] += u' \u2714'
		#adds the unicode tick to the list item
    if args[0] == 'user2' or args[0] == 'user2':
        USER2_TASKS[index] += u' \u2714'
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text='checked :)')
    bot.send_message(chat_id=update.message.chat_id, text=task_print)

def bulkadd(bot, update, args):
    """Add multiple tasks for a specific user"""
    user = args[0]
    args.pop(0)
    args = " ".join(args)
	#join all elements, turning it into one big string
    args = [s.strip() for s in args.split(',')]
	#splits it at the comma and removes the spaces
    for argument in args:
        argument = '- ' + argument
        if user == 'user1' or user == 'user1':
            USER1_TASKS.append(argument)
        if user == 'user2' or user == 'user2':
            USER2_TASKS.append(argument)
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text=task_print)

def bulkcheck(bot, update, args):
    """Put a check beside multiple tasks for a specific user"""
    user = args[0]
    args.pop(0)
	#removes the name of the user from the list
    for argument in args:
        index = int(argument) - 1
        if user == 'user1' or user == 'user1':
            USER1_TASKS[index] += u' \u2714'
        if user == 'user2' or user == 'user2':
            USER2_TASKS[index] += u' \u2714'
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text='all tasks checked :)')
    bot.send_message(chat_id=update.message.chat_id, text=task_print)

def bulkremove(bot, update, args):
    """"Remove multiple tasks for a specific user"""
    user = args[0]
    user = user.lower()
    args.pop(0)
    global USER1_TASKS
    global USER2_TASKS
    for argument in args:
        index = int(argument) - 1
        if user == "user1":
            USER1_TASKS[index] = "BLANK"
        if user == "user2":
            USER2_TASKS[index] = "BLANK"
    #comprehensive list removal of all strings that are equal to "BLANK"
    USER1_TASKS = [s for s in USER1_TASKS if s != "BLANK"]
    USER2_TASKS = [s for s in USER2_TASKS if s != "BLANK"]
    task_print = print_tasks()
    bot.send_message(chat_id=update.message.chat_id, text='tasks cleared x)')
    bot.send_message(chat_id=update.message.chat_id, text=task_print)



TASK_HANDLER = CommandHandler('newtask', tasks, pass_args=True)
 #creates a new command handler that allows arguments to be passed with the telegram command
 #arguments are considered all strings after the initial command
CHECK_HANDLER = CommandHandler('check', check_task, pass_args=True)
CLEAR_HANDLER = CommandHandler('clear', clear)
REMOVE_HANDLER = CommandHandler('remove', remove, pass_args=True)
BATCH_TASK_HANDLER = CommandHandler('bulkadd', bulkadd, pass_args=True)
BATCH_TASK_CHECK_HANDLER = CommandHandler('bulkcheck', bulkcheck, pass_args=True)
BATCH_REMOVE_HANDLER = CommandHandler('bulkremove', bulkremove, pass_args=True)
DISPATCHER.add_handler(TASK_HANDLER)
#adds the newly created handler to the DISPATCHER
#this allows it to be used in the running of the bot
DISPATCHER.add_handler(CHECK_HANDLER)
DISPATCHER.add_handler(CLEAR_HANDLER)
DISPATCHER.add_handler(REMOVE_HANDLER)
DISPATCHER.add_handler(BATCH_TASK_HANDLER)
DISPATCHER.add_handler(BATCH_TASK_CHECK_HANDLER)
DISPATCHER.add_handler(BATCH_REMOVE_HANDLER)
UPDATER.start_polling() #UPDATER starts polling messages and input from the user(s) in the chat
