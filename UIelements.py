import pygame
#import logic
#import random
#import time
import sqlite3
import pickle

#include est adjustments

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
  # 2D array where each row is a list of words.
    words = [word.split(')(') for word in text.splitlines()]  
   # The width of a space.
    space = font.size(' ')[0] 
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

class Button:
  def __init__(self, x, y, text, colour, bg_colour, value_change):
    self.y = y
    self.x = x
    self.displaytext = text
    self.colour = colour
    self.bg_colour = bg_colour
    self.value_change = value_change
    self.smallfont = pygame.font.SysFont('Corbel',35)
    self.text = self.smallfont.render(self.displaytext , True , self.colour, self.bg_colour)
    self.textRect = self.text.get_rect()
    self.textRect.center = (self.x, self.y)
    self.width = self.textRect.w
    self.height = self.textRect.h

  #draws button
  def draw(self, screen):  
    screen.blit(self.text , self.textRect) 

  #value change on button press
  def change(self, mouse):
    #checks mouse position
    if self.x - self.width/2 <= mouse[0] <= self.x + self.width/2 and self.y - self.height/2 <= mouse[1] <= self.y + self.height/2:
      return self.value_change #returns value
    else:
      return 0

class Menu_button(Button):
  #returns true/false on button press
  def change(self, mouse, open):
    if self.x - self.width/2 <= mouse[0] <= self.x + self.width/2 and self.y - self.height/2 <= mouse[1] <= self.y + self.height/2:
      return True
    else:
      return False      

class GreenRedButton(Button):
  def __init__(self, x, y, text, colour, bg_colour, value_change, on_colour):
    #adds the on_colour and active_colour attributes to the child class
    super().__init__(x, y, text, colour, bg_colour, value_change)
    self.on_colour = on_colour
    self.active_colour = self.bg_colour
    
    #now changes the colour of the element based on a True or False input
  def change(self, open):
      if open:
          self.active_colour = self.on_colour
          self.text = self.smallfont.render(self.displaytext , True , self.colour, self.active_colour)
          self.textRect = self.text.get_rect()
      elif not open:
          self.active_colour = self.bg_colour
          self.text = self.smallfont.render(self.displaytext , True , self.colour, self.active_colour)
          self.textRect = self.text.get_rect()

    #setter for the display text
  def setText(self, text): 
    self.displaytext = text

class ActivityNetwork:
  #initialisation
  def __init__(self, tree, width, height, x, y, Nwidth, Nheight, Ncolour, Ncritcolour, Lcolour, Lwidth, maxheight): 
    self.x = x
    self.y = y
    self.tree = tree
    self.width = width
    self.height = height
    self.nodes = []
    self.levelheights = []
    self.maxheight = maxheight
    self.Nwidth = Nwidth
    self.Nheight = Nheight
    self.Ncolour = Ncolour
    self.Lcolour = Lcolour
    self.Lwidth = Lwidth
    self.Ncritcolour = Ncritcolour

  #getters
  def getnodes(self):
    return self.nodes
  
  def get_tree(self):
    return self.tree

  def setupclasses(self):
    #loops through each height of the tree
    for i in range(2, self.maxheight):
      levellen = 0
      #adds up the amount of nodes at the height
      for each in self.tree:
        if each[6] == i:
          levellen += 1
          #adds the height and the amount of nodes at the height to an array
      self.levelheights.append([levellen, i])

    #breaking up the defined width for the network into segments based on how many is needed
    xdif = self.width/len(self.levelheights)
    for level in range(2, self.maxheight):
      group = []
      for each in self.tree:
        if each[6] == level:
          group.append(each)
      #breaking up the height of the network into segments depending on the amount of nodes at a height
      ydif = self.height/len(group)
      #appending the positional information for each node to this array
      for i in range(len(group)):
        self.nodes.append([xdif*(level-2), ydif*(i), group[i]])
      
#50, 50, (50,50,50)

  def draw(self, screen, constraint): # some kind of autoheight and width for text size would be very helpful
    for each in self.nodes:
      #gets the pos of each node to be rendered from self.nodes
      Nx = each[0] + self.x
      Ny = each[1] + self.y + 10
      #creates the text that will be in each nodes box
      Ntext = each[2][0] + str(each[2][4]) + str(each[2][1]) + str(each[2][5]) # needs work
      #draws the box for the node
      pygame.draw.rect(screen, (255,255,255), [Nx - 5, Ny - 5, self.Nwidth + 10, self.Nheight + 10])
      if (each[2][1] + each[2][4]) != each[2][5]:
        pygame.draw.rect(screen, self.Ncolour, [Nx, Ny, self.Nwidth, self.Nheight])
      else:
        pygame.draw.rect(screen, self.Ncritcolour, [Nx, Ny, self.Nwidth, self.Nheight])
      #blits the text using the blit_text function
      blit_text(screen, Ntext, (Nx + 10 ,Ny + 10), pygame.font.Font('freesansbold.ttf', int(16)))

  def draw_arrows(self, screen):
    #loops through each node
    for examinednode in self.nodes:
      #defines the lits for the positions of the successors of the node
      successors_x_y = []
      #gets the sucessors
      successors = examinednode[2][3]
      for nodes in self.nodes:
        for each in successors:
          #gets the position of the sucessor nodes
          if nodes[2][0] == each:
            successors_x_y.append((nodes[0] + self.Nwidth/2 + self.x ,nodes[1] + self.Nheight/2 + self.y))
      for items in successors_x_y:
        #draws a line from the node to ever successor
        pygame.draw.line(screen, self.Lcolour, (examinednode[0] + self.Nwidth/2 + self.x,examinednode[1] + self.Nheight/2 + self.y), items, self.Lwidth)

  #implement moving around screen functions and defined borders where stuff is no longer drawn

  def draw_scale(self, WIN):
    pass
    
class GanttChart(ActivityNetwork):
  def setupclasses(self):
    self.ydif = self.height/(len(self.tree) + 2) + ((self.height/(len(self.tree) + 2)/len(self.tree)))
    self.duration = max([each[5] for each in self.tree])
    self.xdif = self.width/self.duration

    for each in self.tree:
      if each[0] == "START" or each[0] == "END":
        self.tree.remove(each)
    
    for i in range(len(sorted(self.tree, key = lambda x: x[6]))):
      if self.tree[i][0] != "START" and self.tree[i][0] != "END":
        self.nodes.append([self.xdif*(self.tree[i][4]), self.ydif*(i+1), self.tree[i]])

    self.Nheight = self.height/(len(self.nodes)*2)

  def draw(self, screen, constraint): # some kind of autoheight and width for text size would be very helpful
    for each in self.nodes:
      Nx = each[0] + self.x
      Ny = each[1] + self.y

      self.Nwidth = each[2][1] * self.xdif
      
      Ntext = each[2][0] + str(each[2][4]) + str(each[2][1]) + str(each[2][5]) # needs work
      pygame.draw.rect(screen, (255,255,255), [Nx, Ny - 2.5, self.Nwidth + 2.5, self.Nheight + 2.5])
      if (each[2][1] + each[2][4]) != each[2][5]:
        pygame.draw.rect(screen, self.Ncolour, [Nx + 2.5, Ny, self.Nwidth, self.Nheight])
      else:
        pygame.draw.rect(screen, self.Ncritcolour, [Nx + 2.5, Ny, self.Nwidth, self.Nheight])
      blit_text(screen, Ntext, (Nx + 2.5 ,Ny + 2.5), pygame.font.Font('freesansbold.ttf', int(16)))

  def draw_arrows(self, screen):
    for examinednode in self.nodes:
      successors_x_y = []
      successors = examinednode[2][3]
      for nodes in self.nodes:
        for each in successors:
          if nodes[2][0] == each:
            successors_x_y.append((nodes[0] + self.x,nodes[1] + self.Nheight/2 + self.y))
      for items in successors_x_y:
        pygame.draw.line(screen, self.Lcolour, (examinednode[0] + (examinednode[2][1]*self.xdif) + self.x, examinednode[1] + self.Nheight/2 + self.y), (examinednode[0] + (examinednode[2][1]*self.xdif + self.x) + self.y, items[1]), self.Lwidth)
        
        pygame.draw.line(screen, self.Lcolour, ((examinednode[0] + (examinednode[2][1]*self.xdif + self.x), items[1])), items, self.Lwidth)

  def draw_scale(self, screen):
    #scale in steps of 5
    length = max([each[5] for each in self.tree])
    points = length//5 + 1
    scale = self.xdif * 5

    
    for i in range(points + 1):
      pygame.draw.line(screen, (255,255,255), (scale*i + self.x, (self.ydif + self.y - 20)), (scale*i + self.x, (self.ydif -10 + self.y)), 10)
      blit_text(screen, str(5 * i), (scale*i + self.x, (self.ydif + self.y - 30)), pygame.font.Font('freesansbold.ttf', int(16)))
        
  #should make scale lines for x and y axis method

class ResourceHistogram(ActivityNetwork):
  #put constraint into self setup init super

  def setupclasses(self):
    pass

  def draw_arrows(self, screen):
    pass
  
  def draw(self, screen, constraint):
    self.xdif = self.width/max([each[5] for each in self.tree])
    self.ydif = self.height/(max([each[7] for each in self.tree])+self.maxheight) #rebuild this at somepoint to find the highest point of resource usage within the histogram instead of this hacky solution *****
    
    for i in range(max([each[5] for each in self.tree]) + 1):
      set = []
      for each in self.tree:
        if i > each[4] and i <= (each[4] + each[1]):
          if (each[5] - each[1] - each[4]) == 0:
            set.append([each[0], each[7], each[5] - each[1] - each[4], (255,0,0)])
          else:
            set.append([each[0], each[7], each[5] - each[1] - each[4], (255,255,255)])
      set = sorted(set, key = lambda x: x[2])
      height = 0
      for each in set:
        pygame.draw.rect(screen, each[3], [self.x + (self.xdif*(i-1)), self.y + (self.height - (self.ydif*height) - self.ydif*each[1]), self.xdif, self.ydif*each[1]], 0)
        blit_text(screen, each[0], (self.x + (self.xdif*(i-1)), self.y + (self.height - (self.ydif*height) - self.ydif*each[1])), pygame.font.Font('freesansbold.ttf'), int(16))
        height += each[1]
    pygame.draw.line(screen, (0,255,0), (self.x, self.y + (self.height - self.ydif*constraint - 5)), (self.x + self.width, self.y + (self.height - self.ydif*constraint - 5)), 5)

      #make labels, add colour coding maybe?

  def draw_scale(self, screen):
    #scale in steps of 5
    length = max([each[5] for each in self.tree])
    points = length//5 + 1
    scale = self.xdif * 5


    for i in range(points):
      pygame.draw.line(screen, (255,255,255), (scale*i + self.x, (self.ydif + self.y - 20)), (scale*i + self.x, (self.ydif -10 + self.y)), 10)
      blit_text(screen, str(5 * i), (scale*i + self.x, (self.ydif + self.y - 30)), pygame.font.Font('freesansbold.ttf', int(16)))


class InputBox:
  def __init__(self, x, y, w, h, text="", interactable=True):#interactable can be safely removed at later date
      self.colourInactive = (255,255,255)
      self.colourActive = (0,255,0)
      self.FONT = pygame.font.Font(None, 32)
      self.rect = pygame.Rect(x, y, w, h)
      self.color = self.colourInactive
      self.text = text
      self.txt_surface = self.FONT.render(text, True, self.color)
      self.active = False
      self.interactable = interactable

  def handle_event(self, event):
    if self.interactable:
      if event.type == pygame.MOUSEBUTTONDOWN:
          # If the user clicked on the input_box rect.
          if self.rect.collidepoint(event.pos):
              # Toggle the active variable.
              self.active = not self.active
          else:
              self.active = False
          # Change the current color of the input box.
          self.color = self.colourActive if self.active else self.colourInactive
      if event.type == pygame.KEYDOWN:
          if self.active:
              #if event.key == pygame.K_RETURN:
              #    print(self.text)
              #    self.text = ''
              if event.key == pygame.K_BACKSPACE:
                  self.text = self.text[:-1]
              elif self.txt_surface.get_width() + 10 < self.rect.w:
                  self.text += event.unicode.rstrip()

              # Re-render the text.
              self.txt_surface = self.FONT.render(self.text, True, self.color)

 # def update(self):
      # Resize the box if the text is too long.
 #     width = max(200, self.txt_surface.get_width()+10)
 #     self.rect.w = width

  def draw(self, screen):
      # Blit the text.
      screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
      # Blit the rect.
      pygame.draw.rect(screen, self.color, self.rect, 2)

  def getY(self):
    return self.rect.y

  def getText(self):
    return self.text

  def setText(self, text):
    self.text = text
    self.txt_surface = self.FONT.render(self.text, True, self.color)

  def flipActive(self):
    if self.interactable:
      self.interactable = False
    else:
      self.interactable = True

class PopupInputBox(InputBox):
  def handle_event(self, event):
    if self.interactable:
      if event.type == pygame.MOUSEBUTTONDOWN:
          # If the user clicked on the input_box rect.
          if self.rect.collidepoint(event.pos):
              # Toggle the active variable.
              self.active = not self.active
          else:
              self.active = False
          # Change the current color of the input box.
          self.color = self.colourActive if self.active else self.colourInactive
      if event.type == pygame.KEYDOWN:
          if self.active:
              if event.key == pygame.K_RETURN:
                  output = self.text
                  self.text = ""
                  self.txt_surface = self.FONT.render(self.text, True, self.color)
                  return output
              if event.key == pygame.K_BACKSPACE:
                  self.text = self.text[:-1]
              elif self.txt_surface.get_width() + 10 < self.rect.w:
                  self.text += event.unicode.rstrip()

              # Re-render the text.
              self.txt_surface = self.FONT.render(self.text, True, self.color)

    return ""
    
class InputBoxArray:
  def __init__(self, x, y, w, h, tree):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.xdif = w/4
    self.ydif = h/15
    self.tree = tree
    self.box_array = []
  
  def AddRow(self, text = None):
    if text == None and len(self.box_array) <= 15:
        if self.box_array == []:
          self.box_array.append([InputBox(self.x, self.y, self.xdif, self.ydif),  #name
                                 InputBox(self.x + self.xdif, self.y, self.xdif, self.ydif), #duration
                                 InputBox(self.x + self.xdif*2, self.y, self.xdif, self.ydif), #predecessors
                                 InputBox(self.x + self.xdif*3, self.y, self.xdif, self.ydif)]) #resource
  
        else:
          nu_y = self.box_array[-1][0].getY() + self.ydif
          self.box_array.append([InputBox(self.x, nu_y, self.xdif, self.ydif),  #name
                                 InputBox(self.x + self.xdif, nu_y, self.xdif, self.ydif), #duration
                                 InputBox(self.x + self.xdif*2, nu_y, self.xdif, self.ydif), #predecessors
                                 InputBox(self.x + self.xdif*3, nu_y, self.xdif, self.ydif)]) #resource
    elif len(self.box_array) <= 15:
        if self.box_array == []:
          self.box_array.append([InputBox(self.x, self.y, self.xdif, self.ydif, text[0]),  #name
                                 InputBox(self.x + self.xdif, self.y, self.xdif, self.ydif, text[1]), #duration
                                 InputBox(self.x + self.xdif*2, self.y, self.xdif, self.ydif, text[2]), #predecessors
                                 InputBox(self.x + self.xdif*3, self.y, self.xdif, self.ydif, text[3])]) #resource
    
        else:
          nu_y = self.box_array[-1][0].getY() + self.ydif
          self.box_array.append([InputBox(self.x, nu_y, self.xdif, self.ydif, text[0]),  #name
                                 InputBox(self.x + self.xdif, nu_y, self.xdif, self.ydif, text[1]), #duration
                                 InputBox(self.x + self.xdif*2, nu_y, self.xdif, self.ydif, text[2]), #predecessors
                                 InputBox(self.x + self.xdif*3, nu_y, self.xdif, self.ydif, text[3])]) #resource

  def DelRow(self):
    if self.box_array != []:
      del self.box_array[-1]
  
  #DATA FORMAT ["name (input by user)", "duration  (input by user)", "immediate Predecessors (input by user)",  "immediate successors", EST, LFT, Height, resource]
  #need to run exception handling for this bozo
  #fix exceptions
  
  def build_tree(self):
      for row in self.box_array:
        name = row[0].getText()
        duration = int(row[1].getText())
        predecessors = row[2].getText().split(",")
        resource = int(row[3].getText())
        if predecessors == [''] or predecessors == ['START'] or predecessors == ['END']:
          predecessors = []
        if name != "START" and name != "END":
          self.tree.append([name, duration, predecessors, [], None, None, 0, resource])

      return self.tree

  def get_tree(self, tree):
    #clears the input box array
      self.box_array = []
    #loops through the input tree and adds rows based on each node
      for node in tree:
        data = [node[0], str(node[1]), ",".join(node[2]), str(node[7])]
        self.AddRow(data)
        
  def events(self, event):
    for box in self.box_array:
      for each in box:
        each.handle_event(event)
  
  def draw(self, screen):
    for box in self.box_array:
      for each in box:
        each.draw(screen)

  def setTree(self, tree):
    self.tree = tree
  


class SaveBoxArray(InputBoxArray):
    def AddRow(self, text):
      #if the array is not full
      if len(self.box_array) <= 15:
        #if it is the first row
        if self.box_array == []:
          self.box_array.append([InputBox(self.x, self.y, self.xdif, self.ydif, text[0], False),  #ID
                                 InputBox(self.x + self.xdif, self.y, self.xdif, self.ydif, text[1], True), #Name
                                 Menu_button(self.x + self.xdif*2 + 50, self.y + 17, "Load", (0,0,0), (255,255,255), None)]) #Button

    
        else:
          nu_y = self.box_array[-1][0].getY() + self.ydif
          self.box_array.append([InputBox(self.x, nu_y, self.xdif, self.ydif, text[0], False),  #ID
                                 InputBox(self.x + self.xdif, nu_y, self.xdif, self.ydif, text[1], True), #name
                                 Menu_button(self.x + self.xdif*2 + 50, nu_y + 17, "Load", (0,0,0), (255,255,255), None)]) #Button
          
    def get_tree(self, accountID):
        #connects to the database
        connection = sqlite3.connect("activity-tables.db")
        cursor = connection.cursor()
        #fetches the trees related to the input accountID
        output = cursor.execute('''
          SELECT name, TreeID FROM tree WHERE accountID = ?
        ''', (accountID[0][0],)).fetchall()
        print(output)
        connection.commit()
        cursor.close()
        connection.close()

        #clears the self.box_array
        self.box_array = []
        for node in output:
          #adds rows with the data
          data = [str(node[1]), node[0]]
          self.tree.append(data)
          self.AddRow(data)


    def save_trees(self):
        self.tree = []
        #creates the data
        for row in self.box_array:
            data = [row[0].getText(), row[1].getText()]
            self.tree.append(data)
        #connects to the database
        connection = sqlite3.connect("activity-tables.db")
        cursor = connection.cursor()
        #for every element in the tree update the associated record in the tree table
        for each in self.tree:
          input = [each[1],int(each[0])]
          cursor.execute('''
                    UPDATE tree SET name = ? WHERE TreeID = ?
                         ''', input)
        connection.commit()
        cursor.close()
        connection.close()

    def events(self, event, mouse):
      #loops through the box_array
      for box in self.box_array:
        #runs handle event method for the input boxes
        for each in box[:-1]:
          each.handle_event(event)
        #if mouse click detected
        if event.type == pygame.MOUSEBUTTONDOWN:
          #if the load tree button is clicked
          if box[2].change(mouse, False):
            #gets the TreeID from the input box
            TreeID = box[0].getText()
            #loads the treeS
            connection = sqlite3.connect("activity-tables.db")
            cursor = connection.cursor()
            output = cursor.execute('''
              SELECT network, resourceConstraint FROM tree WHERE TreeID = ?
            ''', (TreeID,)).fetchall()
            connection.commit()
            cursor.close()
            connection.close()

            print(output[0][0])

            return pickle.loads(output[0][0]), output[0][1], 3, TreeID
          
      return [], None, 2, None


    

    
