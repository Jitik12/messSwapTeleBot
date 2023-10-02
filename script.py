import os

from telebot.async_telebot import AsyncTeleBot

import sqlite3
from sqlite3 import Error


myToken = os.environ.get("BOT_API_KEY")
bot = AsyncTeleBot(myToken)


def makeDBConnection(dbFile):
  conn = None
  try:
    conn = sqlite3.connect(dbFile)
  except sqlite3.Error as e:
    print(e)
  return conn

# connection = makeDBConnection("./main.db")
# cursor = connection.cursor()

def newUser(name, email, telegramID):
  checkQuerry = 'select * from users where telegramID = "{telegramID}"'.format(telegramID=telegramID)
  try:
    data = cursor.execute(checkQuerry)
    if data != None :
      print("User Found")
      return 0
  except Error as e:
    print(e)
    
  querry = "insert into users values('{name}', '{email}', '{telegramID}')".format(name=name, email=email, telegramID=telegramID)
  try:
    cursor.execute(querry)
    connection.commit()
    return 1
  except sqlite3.Error as e:
    print(e)
  





  
@bot.message_handler(commands=["start", "help"])
async def welcomeUser(message):
  await bot.reply_to(message, "Hello Bitch")
  


# @bot.message_handler(commands=["register"])
# def register(message):
#   newUser()
  
  
# data = cursor.execute("select * from users")
# for each in data :
  # print(each)
  
import asyncio
asyncio.run(bot.polling())
# connection.close()