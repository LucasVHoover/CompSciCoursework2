import sqlite3
#import argon2
import pickle

#do the argon khalyl thingymabob to be able to code in here and amongus

#remember to add commits and closes

def btecArgon(plaintext):
  hash = plaintext
  return hash

def initialiseTables():
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tree(
                TreeID INTEGER PRIMARY KEY,
                AccountID INT,
                name varchar(20) UNIQUE,
                network varchar(1000),
                resourceConstraint INT
                )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords(
                password varchar(50) PRIMARY KEY,
                accountID INT)
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts(
                   accountID INTEGER PRIMARY KEY,
                   username varchar(20) UNIQUE
    )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

def additemstotree(tree, name, accountID):
    input = (accountID, name, pickle.dumps(tree))
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO tree(AccountID, name, network) VALUES(?,?,?,?)''', input
    )

def fetchTree(accountID, name):
    check = (accountID, name)
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    output = cursor.execute("SELECT network FROM tree WHERE accountID = ? AND name = ?", check).fetchall()
    return output

def insertHashword(key, value):
    index = btecArgon(key.encode())
    input = (index, value)
    print(input)
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO passwords VALUES(?,?)''', input
    )
    connection.commit()
    cursor.close()
    connection.close()
 
def checkmatch(key, value):
    index = btecArgon(key.encode())
    input = (index, value)
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    output = cursor.execute(
        '''SELECT accountID FROM passwords WHERE password = ? AND accountID = ?''', input
    ).fetchall()

    connection.commit()
    cursor.close()
    connection.close()
  
    if output != None:
        return True
    else:
        return False

def fetchID(username):
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  output = cursor.execute('''
    SELECT accountID FROM accounts WHERE username = ?
  ''', username).fetchall()
  connection.commit()
  cursor.close()
  connection.close()
  return output
  
