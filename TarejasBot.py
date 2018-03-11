"""
The intention of this program is to provide an easy way for me and my girlfriend,to have a to-do list of items to keep track of and help to increase our productivity. I've made my best attempt to add comments along the code to explain what's going on however if it's still difficult to follow there are additional tutorials linked in the documentation
"""
import datetime, os #adds functionality for printing the date
from telegram.ext import Updater, CommandHandler
os.environ['TZ'] = 'America/New_York' #makes the program recognize the current timezone as mine
updater = Updater(token = 'API-TOKEN')
dispatcher = updater.dispatcher
user1_tasks = []
user2_tasks = []
def printTasks(): #this function constructs the task format and returns a variable the bot can use to print to the users all the tasks to be done
	today = datetime.date.today()
	dateList = []
	dateList.append(today)
	taskPrint = "LIST OF TASKS TO-DO FOR "+str(dateList[0]) #the date is put in a string format for it to be used with the other strings easily
	taskPrint += '\n\nUser1: '
	for i in range(len(user1_tasks)): #runs a loop to gather all the items in the working list
		taskPrint += '\n'
		taskPrint += (user1_tasks[i] + ' ('+str(i+1) + ')') #this adds in brackets the number of the task in the list
	taskPrint += '\n\nUser2: '
	for i in range(len(user2_tasks)):
		taskPrint += '\n'
		taskPrint += (user2_tasks[i]+ ' ('+str(i+1) + ')') #this adds in brackets the number of the task in the list
	return taskPrint

def tasks(bot, update, args): #function declaration. takes the bot and update objects as well as the arguments passed with the command
	if args[0] == 'User1' or args[0] == 'User1':
		args.pop(0) #remove the first argument as it would not be used past knowing what list of tasks to put it in
		args.insert(0,'-')
		args = ' '.join(args) #converts the list of arguments into a single string
		user1_tasks.append(args)	#adds the arguments (minus the name of the individual) to the list of tasks
	if args[0] == 'User2' or args[0] == 'User2':
		args.pop(0)
		args.insert(0,'-')
		args = ' '.join(args)
		user2_tasks.append(args)	
	taskPrint = printTasks()
	bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat


def clear(bot, update): #purpose of this function is to clear the lists
	del user1_tasks[:] 
	del user2_tasks[:]
	taskPrint = printTasks()
	bot.send_message(chat_id=update.message.chat_id, text='Task lists cleared :)')
	bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat


def remove(bot, update, args): #allows the user to erase individual lines
	index = int(args[1]) #passes the second argument to the variable
	index-=1 #users use standard ordinal numbers this converts it to the index form
	if args[0] == 'User1' or args[0] == 'User1':
		user1_tasks.pop(index) #removes the item in the list at that index number
	if args[0] == 'User2' or args[0] == 'User2':
		user2_tasks.pop(index)
	taskPrint = printTasks()
	bot.send_message(chat_id=update.message.chat_id, text='Task cleared :)')
	bot.send_message(chat_id=update.message.chat_id, text=taskPrint) #sends all the content in the taskPrint variable to the chat
	

def check_task(bot, update, args):
	today = datetime.date.today()
	dateList = []
	dateList.append(today)
	index = int(args[1]) #this is the second argument passed to the bot in the command that we're turning into an integer
	index -= 1	#the integer is decremented as the user would not use the index value but the regular numbered value of the item in the list
	if args[0] == 'User1' or args[0] == 'User1':
		user1_tasks[index] += u' \u2714'		#adds the unicode tick to the list item
	if args[0] == 'User2' or args[0] == 'User2':
		user2_tasks[index] += u' \u2714'
	taskPrint = printTasks()
	bot.send_message(chat_id=update.message.chat_id, text='checked :)')
	bot.send_message(chat_id=update.message.chat_id, text=taskPrint) 
	

task_handler = CommandHandler('newtask',tasks,pass_args = True) #creates a new command handler that allows arguments to be passed with the telegram command, arguments are considered all strings after the initial command
check_handler = CommandHandler('check',check_task,pass_args = True)
clear_handler = CommandHandler('clear',clear)
remove_handler = CommandHandler('remove',remove, pass_args = True)
dispatcher.add_handler(task_handler) #adds the newly created handler to the dispatcher. this allows it to be used in the running of the bot
dispatcher.add_handler(check_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(remove_handler)
updater.start_polling() #updater starts polling messages and input from the user(s) in the chat
