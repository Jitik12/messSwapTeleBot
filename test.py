import os

from telebot.async_telebot import AsyncTeleBot

myToken = os.environ.get("BOT_API_KEY")
print(myToken)
bot = AsyncTeleBot(myToken)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
  print("hello")
  await bot.reply_to(message,"Hello Bitch")
  
# @bot.message_handler(commands=['mess'])
# async def ask(message):
#   print("convo = 1")
#   convo = 1
#   await bot.send_message(message.chat.id, "What mess are you in ?")
  
#   if convo == 1:
#     @bot.message_handler(func=lambda mess: mess.text == "old")
#     async def handleOld(message2):
#       print("1")
#       await bot.reply_to(message2, "Do you want to swap to the New Mess ?")
#       convo = 0
#       print("convo = 0")
    
#   if convo == 1:
#     @bot.message_handler(func=lambda mess: mess.text == "new")
#     async def handleNew(message3):
#       print("2")
#       await bot.reply_to(message3, "Do you want to swap to the Old Mess ?")
#       convo = 0
#       print("convo = 0")

@bot.message_handler()
async def messageHandle(message):
  messageArray = message.text.split()
  print(message.text)
  print(messageArray[0])
  print(messageArray[1])
  await bot.reply_to(message, "you said : {mess1} and {mess2}".format(mess1=messageArray[0], mess2=messageArray[1]))

  






import asyncio
asyncio.run(bot.polling())