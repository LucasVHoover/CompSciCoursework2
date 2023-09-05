import pygame

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
    
class Menu:
  def __init__(self, x, y, width, height, colour, text):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.colour = colour
    self.text = text

  #draws menu and text
  def draw(self, screen):
    pygame.draw.rect(screen, (255,255,255), [self.x - 5, self.y - 5, self.width + 10, self.height + 10])
    pygame.draw.rect(screen, self.colour, [self.x, self.y, self.width, self.height])
    blit_text(screen, self.text, (self.x + 10 ,self.y + 10), pygame.font.Font('freesansbold.ttf', int(16)))

  def UpdateText(self,text):
    self.text = text
