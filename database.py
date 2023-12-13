import sqlite3
#import argon2
import pickle

#remember to add commits and closes

def initialiseTables():
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tree(
                TreeID INTEGER PRIMARY KEY,
                AccountID INT,
                name varchar(20),
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
                   username varchar(20)
    )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

#def update_Tree_fields(input, treeID):
    #for node in input:
    #    node.insert(0, treeID)
    #for node in input:
     #   node[3] = ' '.join(node[3])
    #    node[4] = ' '.join(node[4])
    #for i in range(len(input)):
    #    input[i] = tuple(input[i])
    #return input


#def retrieve_fields(output):
#    for i in range(len(output)):
#        output[i] = list(output[i])
#    for node in output:
#        node[5] = node[5].split()
#        node[6] = node[6].split()
#    print(output)
#    TreeID = output[0][0]
##    for each in output:
#            del each[:3]
#    return output, TreeID

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
    index = argon2.hash_password(key.encode())
    input = (index, value)
    print(input)
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO passwords VALUES(?,?)''', input
    )

def checkmatch(key, value):
    index = argon2.hash_password(key.encode())
    input = (index, value)
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    output = cursor.execute(
        '''SELECT accountID FROM passwords WHERE password = ? AND accountID = ?''', input
    ).fetchall()
    if output != None:
        return True
    else:
        return False