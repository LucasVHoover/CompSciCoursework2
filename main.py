import sqlite3
import pygame, sys
from pygame.locals import QUIT
import UIelements
import database
import pickle
import logic
import argon2
from argon2 import PasswordHasher
ph = PasswordHasher()

#Initialising constants
pygame.init()
WIN = pygame.display.set_mode((1500,800))
pygame.display.set_caption('Hello World!')
FPS = 60
clock = pygame.time.Clock()

#creates tables
database.initialiseTables()


connection = sqlite3.connect("activity-tables.db")
cursor = connection.cursor()
output = cursor.execute(
    '''SELECT * FROM accounts'''
).fetchall()
    #pulls the ID
print(output)
output = cursor.execute(
    '''SELECT * FROM passwords'''
).fetchall()
    #pulls the ID
print(output)
connection.commit()
cursor.close()
connection.close()


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

#sets constants
MENU = 0

#MENU 0 - Start Menu
#MENU 1 - Login Screen
#MENU 2 - Load Saved Screen
#MENU 3 - CPA screen
#MENU 4 - Help Screen


logged_in = False

#MENU 0 --------------------------------------------------------------------------------------------------------

#initialises classes

New_Tree = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2, "New Tree", (0,0,0), (255,255,255), None)
Load_Tree = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+50, "Load Tree", (0,0,0), (255,255,255), None)
SignInMenu = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+100, "Log In/Sign Up", (0,0,0), (255,255,255), None)
Help = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/2+150, "Help", (0,0,0), (255,255,255), None)

logo = pygame.image.load("coursework logo.png")
logo = pygame.transform.scale(logo, (600,300))
logomask = pygame.mask.from_surface(logo)

ShowLogin = UIelements.GreenRedButton(100, 100, "Logged In", (255,255,255), (255,0,0), None, (0,255,0)) #Make this a change colour status 
ShowLogin.change(logged_in)

ReturnMain = UIelements.Menu_button(1350, 50, "Main Menu", (0,0,0), (255,255,255), None)

#MENU 1 --------------------------------------------------------------------------------------------------------------------

#sets constants
username = ""
password = ""
infoBoxes = []
accountID = ""
#initialises classes
infoBoxes.append(UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/3, "Username", (0,0,0), (255,255,255), None))
infoBoxes.append(UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/3+100, "Password", (0,0,0), (255,255,255), None))

inputUsername = UIelements.InputBox(WIN.get_width()/2-50, WIN.get_height()/3+20, 100, 40)
inputPassword = UIelements.InputBox(WIN.get_width()/2-50, WIN.get_height()/3+125, 100, 40)

LoginButton = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/3+200, "Login", (0,0,0), (255,255,255), None)

Sign_UpButton = UIelements.Menu_button(WIN.get_width()/2, WIN.get_height()/3+250, "Sign Up", (0,0,0), (255,255,255), None)

#hashes a password
def hashArgon(plaintext):
  hash = ph.hash(plaintext)
  return hash

#checks if a password and hash match
def verifyArgon(hash, plaintext):
    return ph.verify(hash,plaintext)

def insertHashword(key, value):
    #hashes the input
    index = hashArgon(key)
    #creates the input tuple
    input = (index, int(value[0][0]))
    #connects to database
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    #inserts values
    cursor.execute(
        '''INSERT INTO passwords VALUES(?,?)''', input
    )
    connection.commit()
    cursor.close()
    connection.close()
    #closes the connection
 
def checkmatch(password, accountID):
    connection = sqlite3.connect("activity-tables.db")
    cursor = connection.cursor()
    hash = cursor.execute(
        '''SELECT password FROM passwords WHERE accountID = ?''', (accountID[0][0],)
    ).fetchall()
    #pulls the hashed password
    connection.commit()
    cursor.close()
    connection.close()
  
    #if a successful pull return true
    try:
        #verifys argon
        return verifyArgon(hash[0][0], password)
    except:
        return False


def fetchID(username):
  #connects to the database
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor() 
  output = cursor.execute('''
    SELECT * FROM accounts WHERE username = ?
  ''', (username,)).fetchall()
  #gets the account ID
  connection.commit()
  cursor.close()
  connection.close()
  #returns ID
  return output

def Login(): 
    #gets the username and password from the input boxes
    username = inputUsername.getText()
    password = inputPassword.getText()
    print("trying")
    try:
        #gets the account id of the username
        tempID = fetchID(username)
        #checks if the password is correct
        if checkmatch(password, tempID):
            #if it is correct set account id
            accountID = tempID
            #go back to start menu
            MENU = 0
            ShowLogin.change(True)

            print("logged in")

            return MENU, accountID, True
        else:
            return 1, "", True

    #catches any login error
    except:
        print("login error")
        return 1, "", True
        

  
def Sign_Up(): 
    try:
        #gets the username and password from the input boxes
        username = str(inputUsername.getText())
        password = str(inputPassword.getText())
        if username == "" or password == "":
            print("sign in error")
            return 1, "", True

        #connects to the database
        connection = sqlite3.connect("activity-tables.db")
        cursor = connection.cursor()
        #inserts a new record with the input username
        cursor.execute('''
            INSERT OR IGNORE INTO accounts(username) VALUES(?)
        ''', (username,))
        #commits transaction
        connection.commit()
        cursor.close()
        connection.close()

        #gets the ID of this new record
        accountID = fetchID(username)

        #inserts the password of this new account into the hash table
        insertHashword(password, accountID)
        
        #logs in
        MENU , accountID, logged_in = Login()

        return MENU, accountID, logged_in
    except:
        print("sign in error")
        return 1, "", True

#MENU 2 ----------------------------------------------------------------------------------------------------------------------------------------

#initialises classes
SavedBoxes = UIelements.SaveBoxArray(100,100,500,500,[])

#MENU 3 ----------------------------------------------------------------------------------------------------------------------------------------

#setting constants
on_screen = []

constraint = 5
tree = []

view = 1

#view 0 - Activity Netowkr
#view 1 - Gantt Chart

#switch the views between activity network and gantt chart

def setup(tree, view):
#runs the CPA algorithm on the tree and gets the output tree and maxheight
  try:
    tree, maxheight = logic.CPA(tree)

  #uses the on_screen list to contain the active objects 
    if view == 0:
      on_screen.append(UIelements.ResourceHistogram(tree, 800, 400, 550, 350, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
      on_screen.append(UIelements.ActivityNetwork(tree, 800, 400, 550, 0, 50, 50, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
    elif view == 1:
      on_screen.append(UIelements.GanttChart(tree, 800, 400, 550, 0, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))
      on_screen.append(UIelements.ResourceHistogram(tree, 800, 400, 550, 350, 50, 25, (50,50,50), (255,0,0), (0,255,0), 5, maxheight))

#runs setupclasses method for the objects in on_screen
    for each in on_screen:
      each.setupclasses()
  except:
    pass

def switchview(view):
  if view == 0:
    view = 1
  elif view == 1:
    view = 0
  return view

#initialising objects

AddRowButton = UIelements.Menu_button(150, 650, "Add Row", (0,0,0), (255,255,255), None)
BuildTree = UIelements.Menu_button(150, 600, "Build Tree", (0,0,0), (255,255,255), None)
DelRowButton = UIelements.Menu_button(350, 650, "Delete Row", (0,0,0), (255,255,255), None)
SwitchViewButton = UIelements.Menu_button(350, 600, "Switch View", (0,0,0), (255,255,255), None)

SaveAsTree = UIelements.Menu_button(350, 700, "Save As", (0,0,0), (255,255,255), None)
SaveTreeInput = UIelements.PopupInputBox(300,300,100,50,"",False)
SaveTree = UIelements.Menu_button(150, 750, "Save", (0,0,0), (255,255,255), None)
SavePopup = False

LoadTree = UIelements.Menu_button(150, 700, "Load Tree", (0,0,0), (255,255,255), None)

inputBoxes = UIelements.InputBoxArray(0, 34, 500, 500, [])
inputConstraint = UIelements.InputBox(375, 730, 100, 40)

ExampleFormat = UIelements.Menu_button(1350, 100, "EST | Duration | LFT", (0,0,0), (255,255,255), None)

#inputBoxes.get_tree(example)

def saveTree(inputs, name, constraint):
    try:
        #connects to database
        connection = sqlite3.connect("activity-tables.db")
        cursor = connection.cursor()
        input = (accountID[0][0], name, pickle.dumps(inputs), constraint)
        #inserts tree if the name is not identical to an existing tree
        cursor.execute(
            '''INSERT OR IGNORE INTO tree(AccountID, name, network, resourceConstraint) VALUES(?,?,?,?)''', input
        )
        print("Save Complete")
        #commits and returns true if the tree has been saved
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        print("error")
        return False
        
def updateTree(inputs, TreeID, constraint):
    try:
      #connects to database
      connection = sqlite3.connect("activity-tables.db")
      cursor = connection.cursor()
      #setsup input
      input = (pickle.dumps(inputs), constraint, TreeID)
      cursor.execute(
          '''UPDATE tree SET network = ?, resourceConstraint = ? WHERE TreeID = ?''', input
      )
      print("Save Complete")
      #commits change
      connection.commit()
      cursor.close()
      connection.close()
    except:
        print("Save error")
        pass

def loadTree(name):
  #connects to the database
  connection = sqlite3.connect("activity-tables.db")
  cursor = connection.cursor()
  #creates tuple
  check = (accountID[0][0], name)
  #gets the network
  output = cursor.execute("SELECT network, resourceConstraint, TreeID FROM tree WHERE accountID = ? AND name = ?", check).fetchall()
  tree = pickle.loads(output[0][0])
  constraint = output[0][1]
  TreeID = output[0][2]
  #commits changes
  connection.commit()
  cursor.close()
  connection.close()
  #returns tree, constraint and treeID
  return tree, constraint, TreeID

#MENU 4 --------------------------------------------------------------------------------------------------------------------------------

#creating image
helpImage = pygame.image.load("Help-Image.PNG")
helpImage = pygame.transform.scale(helpImage, (900,500))
helpmask = pygame.mask.from_surface(helpImage)

#MAIN LOOP -----------------------------------------------------------------------------------------------------------------------------

while True:
    clock.tick(FPS)
    WIN.fill((10,10,10))
    mouse = pygame.mouse.get_pos()
  
    if MENU == 0:
      #draws all objects
        WIN.blit(logo, (WIN.get_width()/2 - 265, WIN.get_height()/2- 250))
        New_Tree.draw(WIN)
        Load_Tree.draw(WIN)
        SignInMenu.draw(WIN)
        Help.draw(WIN)
        ShowLogin.draw(WIN)
      #gets pygame events
        for event in pygame.event.get():
          #detects if the window is being closed and quits
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
          #if there has been a mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
              #if new tree is clicked
                if New_Tree.change(mouse, False):
                  #check if logged in.
                    if logged_in:
                      #go to the CPA screen
                        on_screen = []
                        inputBoxes.setTree([]) 
                        MENU = 3
              #if sign in clicked
                elif SignInMenu.change(mouse, False):
                  #go to sign in screen
                    MENU = 1
              #if load tree clicked
                elif Load_Tree.change(mouse, False):
                  #if logged in
                    if logged_in:
                      #go to the load tree screen
                        MENU = 2
                      #get saved trees
                        SavedBoxes.get_tree(accountID)
                elif Help.change(mouse, False):
                    MENU = 4

      
    elif MENU == 1:

        #draws all objects
        for each in infoBoxes:
          each.draw(WIN)

        ReturnMain.draw(WIN)
        inputPassword.draw(WIN)
        inputUsername.draw(WIN)
        LoginButton.draw(WIN)
        Sign_UpButton.draw(WIN)
        
        #gets the events
        for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()

          #handles input box events
          inputUsername.handle_event(event)
          inputPassword.handle_event(event)
          
          #checks for button clicks
          if event.type == pygame.MOUSEBUTTONDOWN:
              if LoginButton.change(mouse, False):
                  MENU, accountID, logged_in = Login()

              if Sign_UpButton.change(mouse, False):
                  MENU, accountID, logged_in = Sign_Up()
            
              if ReturnMain.change(mouse, False):
                  MENU = 0
  
                    

  
            
      
    elif MENU == 2:
        #draws the box array and the return main button
        SavedBoxes.draw(WIN)
        ReturnMain.draw(WIN)
        #gets events
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                #runs event method for the save box array
                tree, constraint, MENU, TreeID = SavedBoxes.events(event, mouse)
                #if the tree is being loaded
                if tree != []:
                    #save the tree and get the tree for the input box array
                    SavedBoxes.save_trees()
                    inputBoxes.get_tree(tree)
                    #get the constraint
                    inputConstraint.setText(str(constraint))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #return to main if the return main button is pressed
                    if ReturnMain.change(mouse, False):
                        SavedBoxes.save_trees()
                        MENU = 0

        


    elif MENU == 3:
      #shows prompt to put in name to save
        if SavePopup:
            SaveTreeInput.draw(WIN)
            UIelements.blit_text(WIN, "Input the name of the project you wish to save and press enter:", (172,250), pygame.font.Font('freesansbold.ttf', int(32)))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                saveName = SaveTreeInput.handle_event(event)
            if saveName != "":
              #saves the tree
                if saveTree(tree, saveName, constraint):
                    inputBoxes.setTree([])
                    tree = inputBoxes.build_tree()
                    SaveTreeInput.flipActive()
                    SavePopup = False
                else:
                    SaveTreeInput.flipActive()
                    SavePopup = False
        
        else:
          #draws all items on the screen
            UIelements.blit_text(WIN, "Task Name", (0,0), pygame.font.Font('freesansbold.ttf', int(16)))
            UIelements.blit_text(WIN, "Duration", (125,0), pygame.font.Font('freesansbold.ttf', int(16)))
            UIelements.blit_text(WIN, "Predecessors", (250,0), pygame.font.Font('freesansbold.ttf', int(16)))
            UIelements.blit_text(WIN, "Resources", (375,0), pygame.font.Font('freesansbold.ttf', int(16)))
            UIelements.blit_text(WIN, "Resource Constraint:", (200,740), pygame.font.Font('freesansbold.ttf', int(16)))
            ReturnMain.draw(WIN)
            inputBoxes.draw(WIN)
            AddRowButton.draw(WIN)
            BuildTree.draw(WIN)
            DelRowButton.draw(WIN)
            SaveAsTree.draw(WIN)
            LoadTree.draw(WIN)
            SwitchViewButton.draw(WIN)
            SaveTree.draw(WIN)
            inputConstraint.draw(WIN)
            ExampleFormat.draw(WIN)
            for each in on_screen:
                each.draw_arrows(WIN)
                each.draw(WIN, constraint)
                each.draw_scale(WIN)
              
          #gets events (inputs)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                inputBoxes.events(event)
                inputConstraint.handle_event(event)
              
              #if the event is a click
                if event.type == pygame.MOUSEBUTTONDOWN:
                  #if the mouse is on the location of the button
                    if AddRowButton.change(mouse, False):
                        inputBoxes.AddRow()
                    if DelRowButton.change(mouse, False):
                        inputBoxes.DelRow()
                    if SwitchViewButton.change(mouse, False):
                      #switches the view to the other option
                        view = switchview(view)
                      #clears the networks on screen
                        on_screen = []
                      #clears the input box tree attribute
                        inputBoxes.setTree([])
                        try:
                        #pulls the tree stored in input boxes using build tree
                          tree = inputBoxes.build_tree()
                        #re runs setup with the new view
                          setup(tree, view)
                        except:
                          pass
                    if SaveAsTree.change(mouse, False):
                        #catches any invalid inputs for constraint
                        try:
                          constraint = int(inputConstraint.getText())
                        except:
                          constraint = 0
                        on_screen = []
                        inputBoxes.setTree([]) 
                        tree = inputBoxes.build_tree()
                        SaveTreeInput.flipActive()
                        SavePopup = True
                        saveName = ""

                    if LoadTree.change(mouse, False):
                        MENU = 2
                        on_screen = []
                    if BuildTree.change(mouse, False):
                        #catches erroneous inputs
                        try:
                          constraint = int(inputConstraint.getText())
                        except:
                          constraint = 0
                        on_screen = []
                        inputBoxes.setTree([]) 
                        #prevents total durations to be too large for the algorithm
                        try:
                          tree = inputBoxes.build_tree()
                          if sum([each[1] for each in tree]) > 1000:
                            print("too big duration error")
                          else:
                            setup(tree,view)
                        except:
                            pass
                    if SaveTree.change(mouse, False):
                      #catches invalid inputs
                        try:
                          constraint = int(inputConstraint.getText())
                        except:
                          constraint = 0
                      #saves the tree
                        on_screen = []
                        inputBoxes.setTree([])
                        tree = inputBoxes.build_tree() 
                        updateTree(tree, TreeID, constraint)
                    if ReturnMain.change(mouse, False):
                        MENU = 0
                        on_screen = []
    elif MENU == 4:
         #draw image and text
         WIN.blit(helpImage, (100, 250))
         UIelements.blit_text(WIN, "Welcome To Lucas's CPA, Gantt Chart and Resource Histogram Tool\n\nTo create or load projects you must first sign in.\nTo sign in you must click on log in/sign up\nthen you should input a username and password and press sign up.\nIf you want to log into an existing account acces the same menu and click log in instead\nTo start a new project click new project and to load a saved project select load project.", (100,100), pygame.font.Font('freesansbold.ttf', int(16)))
         #draw return button
         ReturnMain.draw(WIN)
         for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                #detect return input
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ReturnMain.change(mouse, False):
                        MENU = 0
        
                    
                        

                
        

    pygame.display.update()



