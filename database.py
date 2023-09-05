import sqlite3

def initialiseTables():
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tree(
                NodeID INTEGER PRIMARY KEY AUTOINCREMENT,
                TreeID INT,
                name VARCHAR(255),
                duration INT,
                predecessors VARCHAR(255),
                successors VARCHAR(255),
                EST INT,
                LFT INT,
                height INT)
    ''')

def update_Tree_fields(input):
    for node in input:
        node[2] = ' '.join(node[2])
        node[3] = ' '.join(node[3])
    for i in range(len(input)):
        input[i] = tuple(input[i])
    return input

def retrieve_treeID(output):
    return output[0][1]

def retrieve_fields(output):
    for i in range(len(output)):
        output[i] = list(output[i])
    for node in output:
        node[4] = node[4].split()
        node[5] = node[5].split()
    for each in output:
            del each[:2]
    return output

def additemstotree(fields):
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    for p in fields:
        cursor.execute('''
    INSERT INTO tree
                    (name, duration, predecessors, successors, EST, LFT, height)
                    VALUES (?,?,?,?,?,?,?)
                    ''', p)


def fetchTree():
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    output = cursor.execute("SELECT * FROM tree").fetchall()
    treeID = retrieve_treeID(output)
    returned_tree = retrieve_fields(output)
    return returned_tree, treeID