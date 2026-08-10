import pygame;pygame.init()

class Brick:
	def __init__(self,x,y,width,height,color):
		self.rect=pygame.Rect(x,y,width,height)
		self.color=color
	
	def draw(self,win):
		pygame.draw.rect(win,self.color,self.rect)
