import os

from functions2 import *

import mysql.connector

import random

import telebot
from telebot import types

# making the connection to the database 
try:
  database = mysql.connector.connect(
    host = "localhost",
    user = "armaan",
    password = "boggart",
    database = "regisration"
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

newUserObject = {}
emailDeletion = {}

@bot.message_handler(commands=["start"])
def handleStart(message):
  helpMessage = """
  This is a bot developed for the people of IITH for the mess swap system.
  THE MANUAL
  You just 3 commands /register, /swap, /done
  /start 
  /register
  /looking 
  /list
  /swap
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
  try:
    cursor.execute(insertQuerry(user))
    print("User registered => " + insertQuerry(user))
    bot.reply_to(message, "Your name has been registered to our list, Happy Swapping!!!")
    database.commit()
  except:
    print("Error while registration")
    bot.reply_to(message, "There was an Error while Registration")
  

@bot.message_handler(commands=["looking"])
def handleActive(message):
  if findDup(message.chat.id, cursor):
    bot.reply_to(message, 'Your account is already active')
    return
  bot.reply_to(message, "We are making your user active for hunts...")
  question = bot.reply_to(message, "What is your current mess?")
  bot.register_next_step_handler(question, makeActive)

def makeActive(message):
  currentMess = message.text.lower()
  password = random.randint(100_000, 999_999)
  querry = "insert into activeusers values ('{chatID}', '{mess}', '{password}')".format(chatID = message.chat.id ,mess = currentMess, password= password )
  try:
    cursor.execute(querry)
    print("User made active")
    bot.reply_to(message,"Your account is Hunting")
    bot.send_message(message.chat.id , "Your password is {password}".format(password=password))
    database.commit()
    partners = findPartners(currentMess, cursor)
    print(partners)
    for user in partners:
      print(user[0])
      bot.send_message(user[0], "Hola, there is a new swap available, grab her/his password with consent:)")
      print("Notification send")
    bot.send_message(message.chat.id, "We have notified possible partners")
  except:
    bot.reply_to(message, "There was an error while making your account active")
    print("Error while making the user active")
    


@bot.message_handler(commands=["list"])
def handleList(message):
  chatID = message.chat.id
  mess = findMyMess(chatID, cursor)
  print(mess)
  if mess == "user inactive":
    bot.reply_to(message, "You havent applied for swap, so please make your user active for Swap  with /looking")
    return
  
  bot.reply_to(message, f"Your current mess is {mess}")
  partners = findPartners(mess, cursor)
  print(partners)
  returnString = ""
  for each in partners:
    returnString += f"Name : {each[2]} \nEmail : {each[3]}\nUserName : {each[1]}"
    returnString += "\n\n\n"
  try:
    if returnString == "":
      bot.send_message(message.chat.id, "Sorry but there are no user available for swaps")
      return 1
    bot.send_message(message.chat.id, returnString)
    return 0
  except:
    print("Error while printing the partners")
    return 1
    
  
  
@bot.message_handler(commands=["swap"])
def handleSwap(message):
  if findDup(message.chat.id, cursor) == 0:
    bot.reply_to(message, "You are not an active user")
    print("Inactive user tried to swap")
    return
  partners = handleList(message)
  if partners != 0:
    bot.send_message(message.chat.id, "You cant swap at this time, please try again later")
    return
  question = bot.send_message(message.chat.id, "Which one among these do you want to swap with, enter the email address")
  bot.register_next_step_handler(question, handlePassword)

def handlePassword(message):
  partnerEmail = message.text
  emailDeletion[message.chat.id] = partnerEmail
  question = bot.reply_to(message, "Enter the password of your partner")
  bot.register_next_step_handler(question, removeUsers)

def removeUsers(message):
  password = message.text
  chatID = message.chat.id
  partnerEmail = emailDeletion[chatID]
  querry = f"delete from activeusers where chatID = '{chatID}'"
  passwordQuerry = f"delete a from activeusers a join users u on a.chatID = u.chatID where u.email = '{partnerEmail}' and a.password = '{password}'"
  try:
    checkQuerry = f"select a.password from activeusers a join users u on a.chatID = u.chatID where u.email = '{partnerEmail}'"
    cursor.execute(checkQuerry)
    data = cursor.fetchall()
    realPassword = data[0][0]
    if password == realPassword:
      cursor.execute(passwordQuerry)
      cursor.execute(querry)  
      bot.reply_to(message, "Both of you were succesfully swapped")
      print("Both users succesfully swapped")
      database.commit()
    else :
      bot.reply_to(message, "The password you entered was incorrect")
      print("Incorrect password")
  except:
    print("There seems to be an error")
bot.polling()