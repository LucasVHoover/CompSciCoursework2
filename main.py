import sqlite3
import pygame
import UIelements
import database
import logic

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800,800))
pygame.display.set_caption('Hello World!')

#DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height]
input = [['A',7, [], [], None, None, 0],
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

database.initialiseTables()
database.additemstotree(input, 1)
tree, treeID = database.fetchTree()

tree = logic.Immediate_Successors(tree)
tree = logic.StartEnd_Nodes(tree)
tree = logic.height(tree, 1)
maxheight = logic.maxheights(tree)
tree = logic.forwardPass(tree, 2, maxheight)
tree = logic.LFT_EndNode(tree, maxheight)
tree = logic.backwardPass(tree, maxheight-1)
print(tree)
CPtree = logic.criticalPathTree(tree)
print(CPtree)

#database.initialiseTables()
#database.insertHashword('hello goober', 123)
#print(database.checkmatch('hello goober', 123))

