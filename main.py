import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)

import pygame;pygame.init();pygame.font.init()
import random
from bricks import Brick
import time

WIDTH,HEIGHT=800,800
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Brick Breaker')
clock=pygame.time.Clock()
FONT=pygame.font.SysFont('Comic Sans MS',50)

WHITE="#FFFFFF"
BLACK="#000000"
RED="#FF0008"
GREEN="#007539"
BLUE="#1F00D1"

pw,ph=100,10
px,py=(WIDTH/2)-(pw/2),HEIGHT-100

bs=7
bx,by=(WIDTH/2)-(bs/2),(HEIGHT/2)-(bs/2)

brickw,brickh=80,20
ROWS=9
COLS=6
padding=5
topOffset=50

bricks=[]

playerspeed=5

def getdirection():
	direction=random.randint(0,1)
	if direction==0:
		bvx,bvy=-3,5
	elif direction==1:
		bvx,bvy=3,5
	return bvx,bvy

bvx,bvy=getdirection()

WIN.fill(BLACK)

def choosecolor():
	colorchoice=random.randint(0,2)
	if colorchoice==0:
		return RED
	elif colorchoice==1:
		return GREEN
	elif colorchoice==2:
		return BLUE

for row in range(ROWS):
		for col in range(COLS):
			color=choosecolor()
			x=row*(brickw+padding)+20
			y=col*(brickh+padding)+topOffset
			bricks.append(Brick(x,y,brickw,brickh,color))

lose_message=FONT.render('You Lose!',True,WHITE)
win_message=FONT.render('You Win!',True,WHITE)
start_message=FONT.render('Press space to start',True,WHITE)
gameOver_message=FONT.render('Press r to restart or q to quit.',True,WHITE)

lives=3

state='menu'

def restart():
	global bx,by,bvx,bvy,lives,bricks
	bx,by=(WIDTH/2)-(bs/2),(HEIGHT/2)-(bs/2)
	bvx,bvy=getdirection()
	lives=3
	bricks=[]
	for row in range(ROWS):
		for col in range(COLS):
			color=choosecolor()
			x=row*(brickw+padding)+20
			y=col*(brickh+padding)+topOffset
			bricks.append(Brick(x,y,brickw,brickh,color))

run=True
while run:
	clock.tick(60)
	WIN.fill(BLACK)

	if state=='menu':
		WIN.blit(start_message,((WIDTH/2)-(start_message.get_width()/2),(HEIGHT/2)-(start_message.get_height()/2)))
		pass
	
	elif state=='playing':
		player=pygame.Rect(px,py,pw,ph)
		ball=pygame.Rect(bx,by,bs,bs)

		by+=bvy;bx+=bvx
		if player.colliderect(ball):
			by=py-bs
			bvy*=-1
		
		if bx<0:
			bvx*=-1
		elif bx>(WIDTH-bs):
			bvx*=-1
		if by<0:
			bvy*=-1
		elif by>HEIGHT-bs:
			lives-=1
			bvx,bvy=getdirection()
			bx,by=(WIDTH/2)-(bs/2),(HEIGHT/2)-(bs/2)
			
		if px<0:
			px=0
		elif px>(WIDTH-pw):
			px=(WIDTH-pw)
		
		pygame.draw.rect(WIN,WHITE,player)
		pygame.draw.rect(WIN,WHITE,ball)

		for i in range(lives):
			pygame.draw.circle(WIN,RED,((i+1)*20,HEIGHT-50),10)
		
		for brick in bricks:
			brick.draw(WIN)

		hit_brick=None
		for brick in bricks:
			if ball.colliderect(brick.rect):
				hit_brick=brick
				break
		if hit_brick:
			bvy*=-1
			bricks.remove(hit_brick)
		
		if lives<=0:
			state='lost'

		if len(bricks)==0:	
			state='won'
	
	elif state=='lost':
		WIN.blit(lose_message,((WIDTH/2)-(lose_message.get_width()/2),(HEIGHT/2)-(lose_message.get_height()/2)))
		WIN.blit(gameOver_message,((WIDTH/2)-(gameOver_message.get_width()/2),(HEIGHT/2)-(gameOver_message.get_height()/2)+100))
		pygame.display.update()
	elif state=='won':
		WIN.blit(win_message,((WIDTH/2)-(win_message.get_width()/2),(HEIGHT/2)-(win_message.get_height()/2)))
		WIN.blit(gameOver_message,((WIDTH/2)-(gameOver_message.get_width()/2),(HEIGHT/2)-(gameOver_message.get_height()/2)+100))
		pygame.display.update()
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_q:
				run=False
			if state=='menu' and event.key==pygame.K_SPACE:
				state='playing'
			elif (state=='lost' or state=='won') and event.key==pygame.K_r:
				restart()
				state='playing'

	keys=pygame.key.get_pressed()
	if keys[pygame.K_RIGHT]:
		px+=playerspeed
	if keys[pygame.K_LEFT]:
		px-=playerspeed

	pygame.display.update()
pygame.quit()
