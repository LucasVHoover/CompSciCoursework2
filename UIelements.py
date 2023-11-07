import pygame
import logic

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(')(') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
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
    self.text = text
    self.colour = colour
    self.bg_colour = bg_colour
    self.value_change = value_change
    self.smallfont = pygame.font.SysFont('Corbel',35)
    self.text = self.smallfont.render(self.text , True , self.colour, self.bg_colour)
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
    
#class node:
#  def __init__(self, x, y, width, height, item, colour): #just use a list idiot
#    self.x = x
#    self.y = y
#    self.width = width
#    self.height = height
#    self.item = item
#    self.colour = colour
#    self.text = item[0] + str(item[4]) + str(item[1]) + str(item[5])#
#
#  #draws and text
#  def draw(self, screen):
#    pygame.draw.rect(screen, (255,255,255), [self.x - 5, self.y - 5, self.width + 10, self.height + 10])
#    pygame.draw.rect(screen, self.colour, [self.x, self.y, self.width, self.height])
#    blit_text(screen, self.text, (self.x + 10 ,self.y + 10), pygame.font.Font('freesansbold.ttf', int(16)))
  
  
class ActivityNetwork:
  def __init__(self, tree, width, height, x, y, Nwidth, Nheight, Ncolour, Ncritcolour, Lcolour, Lwidth): 
    self.x = x
    self.y = y
    self.tree = tree
    self.width = width
    self.height = height
    self.nodes = []
    self.levelheights = []
    self.maxheight = None
    self.Nwidth = Nwidth
    self.Nheight = Nheight
    self.Ncolour = Ncolour
    self.Lcolour = Lcolour
    self.Lwidth = Lwidth
    self.Ncritcolour = Ncritcolour


  def getnodes(self):
    return self.nodes
  
  def get_tree(self):
    return self.tree

  def CPA(self):
    self.tree = logic.Immediate_Successors(self.tree)
    self.tree = logic.StartEnd_Nodes(self.tree)
    self.tree = logic.height(self.tree, 1)
    self.maxheight = logic.maxheights(self.tree)
    self.tree = logic.forwardPass(self.tree, 2, self.maxheight)
    self.tree = logic.LFT_EndNode(self.tree, self.maxheight)
    self.tree = logic.backwardPass(self.tree, self.maxheight-1)
    print("self.tree is: ", self.tree)

    for i in range(2, self.maxheight):
      levellen = 0
      for each in self.tree:
        if each[6] == i:
          levellen += 1
      self.levelheights.append([levellen, i])

  def setupclasses(self):
    xdif = self.width/len(self.levelheights)
    for level in range(2, self.maxheight):
      group = []
      for each in self.tree:
        if each[6] == level:
          group.append(each)
      print(group)
      ydif = self.height/len(group)
      for i in range(len(group)):
        self.nodes.append([xdif*(level-1), ydif*(i+1), group[i]])

#50, 50, (50,50,50)

  def draw(self, screen):
    for each in self.nodes:
      Nx = each[0]
      Ny = each[1]
      Ntext = each[2][0] + str(each[2][4]) + str(each[2][1]) + str(each[2][5])
      pygame.draw.rect(screen, (255,255,255), [Nx - 5, Ny - 5, self.Nwidth + 10, self.Nheight + 10])
      if (each[2][1] + each[2][4]) != each[2][5]:
        pygame.draw.rect(screen, self.Ncolour, [Nx, Ny, self.Nwidth, self.Nheight])
      else:
        pygame.draw.rect(screen, self.Ncritcolour, [Nx, Ny, self.Nwidth, self.Nheight])
      blit_text(screen, Ntext, (Nx + 10 ,Ny + 10), pygame.font.Font('freesansbold.ttf', int(16)))

  def draw_arrows(self, screen):
    for examinednode in self.nodes:
      successors_x_y = []
      successors = examinednode[2][3]
      for nodes in self.nodes:
        for each in successors:
          if nodes[2][0] == each:
            successors_x_y.append((nodes[0] + self.Nwidth/2,nodes[1] + self.Nheight/2))
      for items in successors_x_y:
        pygame.draw.line(screen, self.Lcolour, (examinednode[0] + self.Nwidth/2,examinednode[1] + self.Nheight/2), items, self.Lwidth)
    
