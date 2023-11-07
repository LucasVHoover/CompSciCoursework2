import sqlite3
import pygame, sys
from pygame.locals import QUIT
import UIelements
import database
import logic
import pickle

pygame.init()
WIN = pygame.display.set_mode((1600,800))
pygame.display.set_caption('Hello World!')
FPS = 60
clock = pygame.time.Clock()

database.initialiseTables()

#DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height]
inputs = [['A',7, [], [], None, None, 0],
        ['B', 6, [], [], None, None, 0],
        ['C',  15, [],[], None, None,0],
        ['D',  9, ['A', 'B'],[], None, None,0],
        ['E',  8, ['D'],[], None, None,0],
        ['F', 6, ['C', 'D'],[], None, None, 0],
        ['G',  7, ['C'],[], None, None,0],
        ['H',  14, ['E'],[], None, None,0],
        ['I',  17, ['F', 'G'],[], None, None,0],
        ['J',  9, ['H','I'],[], None, None,0],
        ['K',  8, ['I'],[], None, None,0],
        ['L',  12, ['J', 'K'],[], None, None,0]]

check = (1, "bob")
connection = sqlite3.connect("activity-tables.db")
cursor = connection.cursor()
input = (1, "bob", pickle.dumps(inputs))
cursor.execute(
    '''INSERT INTO tree(AccountID, name, network) VALUES(?,?,?)''', input
)

output = cursor.execute("SELECT network FROM tree WHERE accountID = ? AND name = ?", check).fetchall()
tree = pickle.loads(output[0][0])

#tree = logic.Immediate_Successors(tree)
#tree = logic.StartEnd_Nodes(tree)
#tree = logic.height(tree, 1)
#maxheight = logic.maxheights(tree)
#tree = logic.forwardPass(tree, 2, maxheight)
#tree = logic.LFT_EndNode(tree, maxheight)
#tree = logic.backwardPass(tree, maxheight-1)
#print(tree)
#CPtree = logic.criticalPathTree(tree)
#print(CPtree)

network = UIelements.ActivityNetwork(tree, 800, 500, 100, 100, 50, 50, (50,50,50), (255,0,0), (255,255,255), 10)
network.CPA()
print(network.levelheights)
network.setupclasses()
print(network.nodes)


while True:
    clock.tick(FPS)
    WIN.fill((10,10,10))
    network.draw_arrows(WIN)
    network.draw(WIN)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()



#database.initialiseTables()
#database.insertHashword('hello goober', 123)
#print(database.checkmatch('hello goober', 123))

