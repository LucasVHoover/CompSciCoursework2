import sqlite3
import pygame, sys
from pygame.locals import QUIT
import UIelements
import database
import pickle
import logic

pygame.init()
WIN = pygame.display.set_mode((1500,1000))
pygame.display.set_caption('Hello World!')
FPS = 60
clock = pygame.time.Clock()

database.initialiseTables()


#DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height, resource]

example = [['A',7, [], [], None, None, 0, 1],
  ['B', 6, [], [], None, None, 0, 1],
  ['C',  15, [],[], None, None,0, 1],
  ['D',  9, ['A', 'B'],[], None, None,0, 1],
  ['E',  8, ['D'],[], None, None,0,1],
  ['F', 6, ['C', 'D'],[], None, None, 0,1],
  ['G',  7, ['C'],[], None, None,0,1],
  ['H',  14, ['E'],[], None, None,0,1],
  ['I',  17, ['F', 'G'],[], None, None,0,1],
  ['J',  9, ['H','I'],[], None, None,0,1],
  ['K',  8, ['I'],[], None, None,0,1],
  ['L',  12, ['J', 'K'],[], None, None,0,1]]


MENU = 0

#MENU 0 - Start Menu
#MENU 1 - Login Screen
#MENU 2 - Load Saved Screen
#MENU 3 - Loaded thingmabob

view = 1

#view 0 - Activity Netowkr
#view 1 - Gantt Chart

#switch the views between activity network and gantt chart

logged_in = False

#MENU 0 -------------------------------------------------------------------------------------------------------------------

New_Tree = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2, "New Tree", (0,0,0), (255,255,255), None)
Load_Tree = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+50, "Load Tree", (0,0,0), (255,255,255), None)
SignInMenu = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+100, "Log In/Sign Up", (0,0,0), (255,255,255), None)
Help = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+150, "Help", (0,0,0), (255,255,255), None)

logo = pygame.image.load("coursework logo.png")
logomask = pygame.mask.from_surface(logo)

ShowLogin = UIelements.GreenRedButton(100, 100, "Logged In", (255,255,255), (255,0,0), None, (0,255,0)) #Make this a change colour status 
ShowLogin.change(logged_in)

#MENU 1 --------------------------------------------------------------------------------------------------------------------

username = ""
password = ""
infoBoxes = []
infoBoxes.append(UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2, "Username", (0,0,0), (255,255,255), None))
infoBoxes.append(UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+100, "Password", (0,0,0), (255,255,255), None))

inputUsername = UIelements.InputBox(WIN.get_width()/2-50, WIN.get_height()/2+20, 100, 40) #these should be resizable. Make this so
inputPassword = UIelements.InputBox(WIN.get_width()/2-50, WIN.get_height()/2+125, 100, 40)

LoginButton = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+200, "Login", (0,0,0), (255,255,255), None)

Sign_UpButton = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+250, "Sign Up", (0,0,0), (255,255,255), None)

def Login():
  username = inputUsername.getText()
  password = inputPassword.getText()
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  AccountID = cursor.execute(
    '''SELECT AcconutID
       FROM accounts
       WHERE username = ?''', username
  )
  #needs finishing requiring argon3 hash

  connection.commit()
  cursor.close()
  connection.close()

def Sign_Up():
  username = inputUsername.getText()
  password = inputPassword.getText()
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  cursor.execute('''
    INSERT INTO accounts(username) VALUES(?)
  ''', username)

  #needs finishing requiring argon3 hash
  
  connection.commit()
  cursor.close()
  connection.close()

#MENU 2 ----------------------------------------------------------------------------------------------------------------------------------------

#MENU 3 ----------------------------------------------------------------------------------------------------------------------------------------

on_screen = []

constraint = 5
tree = []


def setup(tree, view):
  print(tree)
  tree, maxheight = logic.CPA(tree)

  if view == 0:
    on_screen.append(UIelements.ResourceHistogram(tree, 800, 400, 550, 350, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
    on_screen.append(UIelements.ActivityNetwork(tree, 800, 400, 550, 0, 50, 50, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
  elif view == 1:
    on_screen.append(UIelements.GanttChart(tree, 800, 400, 550, 0, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
    on_screen.append(UIelements.ResourceHistogram(tree, 800, 400, 550, 350, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))

  for each in on_screen:
    each.setupclasses()

def switchview(view):
  if view == 0:
    view = 1
  elif view == 1:
    view = 0
  return view

#potential convert this set into dictionary?

AddRowButton = UIelements.Menu_button(150, 650, "Add Row", (0,0,0), (255,255,255), None)
BuildTree = UIelements.Menu_button(150, 600, "Build Tree", (0,0,0), (255,255,255), None)
DelRowButton = UIelements.Menu_button(350, 650, "Delete Row", (0,0,0), (255,255,255), None)
SwitchViewButton = UIelements.Menu_button(350, 600, "Switch View", (0,0,0), (255,255,255), None)

SaveAsTree = UIelements.Menu_button(350, 700, "Save As", (0,0,0), (255,255,255), None)
SaveTreeInput = UIelements.PopupInputBox(300,300,100,50,"",False)
SavePopup = False

LoadTree = UIelements.Menu_button(150, 700, "Load Tree", (0,0,0), (255,255,255), None)
LoadTreeInput = UIelements.PopupInputBox(300,300,100,50,"",False)
LoadPopup = False

inputBoxes = UIelements.InputBoxArray(0, 0, 500, 500, [])

#inputBoxes.get_tree(example)

def saveTree(inputs, constraint, name):
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  input = (1, name, pickle.dumps(inputs), constraint)
  cursor.execute(
      '''INSERT INTO tree(AccountID, name, network, resourceConstraint) VALUES(?,?,?,?)''', input
  )
  print("Save Complete")
  connection.commit()
  cursor.close()
  connection.close()

def loadTree(name):
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  check = (1, name)
  output = cursor.execute("SELECT network, resourceConstraint FROM tree WHERE accountID = ? AND name = ?", check).fetchall()
  tree = pickle.loads(output[0][0])
  constraint = output[0][1]
  connection.commit()
  cursor.close()
  connection.close()
  return tree, constraint

while True:
    clock.tick(FPS)
    WIN.fill((10,10,10))
    mouse = pygame.mouse.get_pos()
    if MENU == 0:
        New_Tree.draw(WIN)
        Load_Tree.draw(WIN)
        SignInMenu.draw(WIN)
        Help.draw(WIN)
        ShowLogin.draw(WIN)
      
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if New_Tree.change(mouse, False):
                    MENU = 3
                if SignInMenu.change(mouse, False):
                    MENU = 1

      
    elif MENU == 1:

        for each in infoBoxes:
          each.draw(WIN)

        inputPassword.draw(WIN)
        inputUsername.draw(WIN)
        LoginButton.draw(WIN)
        Sign_UpButton.draw(WIN)
        
        for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              if LoginButton.change(mouse, False):
                  MENU = 0
      
    elif MENU == 2:
        pass
    elif MENU == 3:
        
        if SavePopup:
            SaveTreeInput.draw(WIN)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                saveName = SaveTreeInput.handle_event(event)
            if saveName != "":
                inputBoxes.tree = []
                tree = inputBoxes.build_tree()
                SaveTreeInput.flipActive()
                SavePopup = False
                saveTree(tree, constraint, saveName)
        elif LoadPopup:
            LoadTreeInput.draw(WIN)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                loadName = LoadTreeInput.handle_event(event)
            if loadName != "":
                LoadTreeInput.flipActive()
                LoadPopup = False
                loadedtree, constraint = loadTree(loadName)
                inputBoxes.get_tree(loadedtree)
        
        else:
            inputBoxes.draw(WIN)
            AddRowButton.draw(WIN)
            BuildTree.draw(WIN)
            DelRowButton.draw(WIN)
            SaveAsTree.draw(WIN)
            LoadTree.draw(WIN)
            SwitchViewButton.draw(WIN)
            for each in on_screen:
                each.draw_arrows(WIN)
                each.draw(WIN, constraint)
                each.draw_scale(WIN)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                inputBoxes.events(event)
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if AddRowButton.change(mouse, False):
                        inputBoxes.AddRow()
                    if DelRowButton.change(mouse, False):
                        inputBoxes.DelRow()
                    if SwitchViewButton.change(mouse, False):
                        view = switchview(view)
                        on_screen = []
                        inputBoxes.tree = []
                        tree = inputBoxes.build_tree()
                        setup(tree, view)
                    if SaveAsTree.change(mouse, False):
                        SaveTreeInput.flipActive()
                        SavePopup = True
                        saveName = ""
                    if LoadTree.change(mouse, False):
                        LoadTreeInput.flipActive()
                        LoadPopup = True
                        loadName = ""
                    if BuildTree.change(mouse, False):
                        on_screen = []
                        inputBoxes.tree = [] #setup getters and setters in future
                        tree = inputBoxes.build_tree()
                        setup(tree,view)
                
        

    pygame.display.update()



#database.initialiseTables()
#database.insertHashword('hello goober', 123)
#print(database.checkmatch('hello goober', 123))

