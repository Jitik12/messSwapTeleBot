def insertQuerry(newUser):
  querry = "insert into users values ('{chatID}', '{telegramID}', '{name}', '{email}')".format(chatID=newUser.chatID, telegramID=newUser.telegramID, name=newUser.name, email=newUser.email)
  return querry

def findDup(chatID, cursor):
  ans = 0
  checkQuerry = f"select * from activeusers where chatID = '{chatID}'"
  cursor.execute(checkQuerry)
  data = cursor.fetchall()
  if len(data) != 0:
    ans = 1
  return ans

def findMyMess(chatID, cursor):
  querry = f"select mess from activeusers where chatID = '{chatID}'"
  try:
    cursor.execute(querry)
    data = cursor.fetchall()
    if len(data) == 1:
      print("User applying for swap... User spotted... Fetching his current mess...")
      return data[0][0]
    elif len(data) == 0:
      print("UnRegistered user asking for list of partners")
      return "user inactive"
    else:
      print("There is an Error in the DB... Multiple records found")
      return "Bad DB"
  except:
    print("You havent registered yet")
    return "Error in finding partners"
  
def findPartners(mess, cursor):
  querry = f"select * from users u join activeusers a on u.chatID = a.chatID where a.mess != '{mess}'"
  cursor.execute(querry)
  try:
    partners = cursor.fetchall()
    if len(partners) != 0:
      return partners
    else:
      print("No partners found")
      print("jello")
      return []
  except:
    print("Error while finding partners")
    return []
  
  
def deleteQuery(chatID):
  querry = f"delete from users where chatID = '{chatID}'"
  return querry