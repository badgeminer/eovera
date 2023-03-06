import pygame, sys,math
from enum import Enum,auto 
from random import randint
from pygame.locals import QUIT

pygame.init()
scr = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
arc = pygame.sprite.LayeredUpdates()
eng = pygame.sprite.LayeredUpdates()
ui = pygame.sprite.LayeredUpdates()
white = pygame.Surface((10,10))
white.fill((255,255,255))

class upd(Enum):
  click = auto()
  boom = auto()

class assets:
  def __init__(self):
    self.detonate = pygame.transform.scale(pygame.image.load("assets/detonate.png"),(25,25))
    self.explosive = pygame.transform.scale(pygame.image.load("assets/explosive.png"),(25,25))

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    def print(self, screen, text,col):
        print(col)
        text_bitmap = self.font.render(text, True, col)
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

class obj(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, img,x_y=(0,0)):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = img

       self.rect = self.image.get_rect()
       self.rect.topleft = x_y
    def update(self,type,**args):
      global score
      if type == upd.click:
        pos = args["pos"]
        if self.rect.collidepoint(pos[0],pos[1]):
          self.kill()
          score += 2
      elif type == upd.boom:
        pos = args["rect"]
        if self.rect.colliderect(pos):
          self.kill()
          score += 1


arc.add(obj(white,(randint(2,398),randint(2,298))))
arc.add(obj(white,(randint(2,398),randint(2,298))))
tp = TextPrint()
score = 0
class text:
  def __init__(self,text):
    self.expire = 2
    self.text = text
    self.col = pygame.Color(255,255,255,255)
textls = []
blackcol = pygame.Color(255,255,255,0)
clk = pygame.time.Clock()

asset = assets()

eng.add(obj(asset.explosive,(50,200)))
ui.add(obj(asset.explosive,(30,275)))
ui.add(obj(asset.detonate,(0,275)))

while True:
    delta = clk.tick(30)/1000
    tp.reset()
    scr.fill((0,0,5))
    tp.tprint(scr,"score:"+str(score))
    for i in textls:
      i.expire -= delta
      if i.expire > 0:
        i.col.update(i.col.lerp(blackcol,(i.expire/2)))
        tp.tprint(scr,i.text)
      else:
        textls.remove(i)
    arc.draw(scr)
    eng.draw(scr)
    ui.draw(scr)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_p:
            arc.add(obj(white,(randint(2,398),randint(2,298))))
          elif event.key == pygame.K_b:
            p = pygame.mouse.get_pos()
            textls.append(text("explosives -5"))
            score -= 5
            arc.update(upd.boom,rect=(p[0]-20,p[1]-20,40,40))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            arc.update(upd.click,pos=event.pos)
    pygame.display.update()