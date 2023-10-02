import os

from functions import *

import mysql.connector

import telebot
from telebot import types

# making the connection to the database 
try:
  database = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    database = os.environ.get("DB_NAME")
  )
  cursor = database.cursor()
  print("DB connected")
except:
  print("Connection unsuccessful")

# bot related stuff
myToken = os.environ.get("BOT_API_KEY")

bot = telebot.TeleBot(myToken)


class User :
  def __init__(self):
    self.chatID = None
    self.telegramID = None
    self.name = None
    self.email = None
    self.mess = None

newUserObject = {}

@bot.message_handler(commands=["start"])
def handleStart(message):
  helpMessage = """
  This is a bot developed for the people of IITH for the mess swap system.
  THE MANUAL
  You just 3 commands /register, /swap, /done
  /register => it just means that you are looking for and are applying for a swap
  /list => it just gives you a list of the bros of the opposite mess who are looking for a swap like you ma bro
  /swap => it just deletes your name and the name of your partner from the list, thats all
  """
  bot.send_message(message.chat.id,helpMessage)


@bot.message_handler(commands=["register"])
def handleRegister(message):
  if findDup(message.chat.id, cursor) == 1:
    print("Duplicate Found")
    bot.reply_to(message, "Accounts can't be used to make more than one registration")
    return
  question = bot.reply_to(message, "Hola user, what might you be called?")
  bot.register_next_step_handler(question, handleName)

def handleName(message):
  user = User()
  user.name = message.text
  user.chatID = message.chat.id
  user.telegramID = message.chat.username
  newUserObject[message.chat.id] = user
  question = bot.reply_to(message, "I wonder what your institute mailID is...")
  bot.register_next_step_handler(question, handleEmail)

def handleEmail(message):
  user = newUserObject[message.chat.id]
  user.email = message.text
  question = bot.reply_to(message, "What's your curren mess?\nOptions are 'udh' or 'ldh'(all-small-case)")
  bot.register_next_step_handler(question, handleMess)
  
def handleMess(message):
  user = newUserObject[message.chat.id]
  user.mess = message.text.lower()
  try:
    cursor.execute(insertQuerry(user))
    print("User registered => " + insertQuerry(user))
    bot.reply_to(message, "Your name has been registered to our list, Happy Swapping!!!")
    database.commit()
  except:
    print("Error while registration")
    bot.reply_to(message, "There was an Error while Registration")
  
  
  
@bot.message_handler(commands=["list"])
def handleSwaps(message):
  chatID = message.chat.id
  mess = findMyMess(chatID, cursor)
  if mess == "unregistered user":
    bot.reply_to(message, "You havent applied for swap, so please register for Swap First with /register")
    return
  
  bot.reply_to(message, f"Your current mess is {mess}")
  partners = findPartners(mess, cursor)
  print(partners)
  returnString = ""
  for each in partners:
    returnString += f"Name : {each[2]} \nEmail : {each[3]}\nUserName : {each[1]}"
    returnString += "\n\n\n"
  bot.send_message(message.chat.id, returnString)
  
  
@bot.message_handler(commands=["swap"])
def handleDone(message):
  chatID = message.chat.id
  mess = findMyMess(chatID, cursor)
  if findDup(chatID, cursor) == 0:
    print("Your name doesnt exist in the DB")
    bot.reply_to(message,"Your name doesnt exist in the db, start with registration with /register")
    return
  
  try:
    partners = findPartners(mess, cursor)
    if len(partners) == 0:
      print("Applied for swap, no partners found")
      bot.reply_to(message, "There are no partners for you to swap with...Sorry:(")
      return
    returnString = ""
    for each in partners:
      returnString += f"Name : {each[2]} \nEmail : {each[3]}\nUserName : {each[1]}"
      returnString += "\n\n\n"
    bot.send_message(message.chat.id, returnString)
    question = bot.reply_to(message, "Which one among the above do you want to swap with? Enter their email.")
    bot.register_next_step_handler(question, actuallyDelete)
  except:
    print("Error while getting all your possible partners")

def actuallyDelete(message):
  finalPartnerEmail = message.text
  querryForPartner = f"delete from users where email = '{finalPartnerEmail}'" 
  querryForMain = f"delete from users where chatID = '{message.chat.id}'"
  try:
    cursor.execute(querryForPartner)
    cursor.execute(querryForMain)
    database.commit()   
    print("User and the Partner succesfully swapped")
    bot.reply_to(message, "Congratulations on the SWAP")
  except:
    print("Error while deleting the mainUser and the partner...")
    
bot.polling()
  
  