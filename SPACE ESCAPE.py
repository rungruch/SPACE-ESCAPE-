
import pygame
import os
import random

# GEOMETRY

WIDTH = 800
HEIGHT = 600
FPS = 60 #Frame Rate per second

# COLOR

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SEA = (159, 192, 245)
GREEN = (72, 232, 152)
GREY = (28, 28 , 28)

#Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space escape??')
clock = pygame.time.Clock()

######CREATE SUBMARINE#######
game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'pic')
print(game_folder)


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def newene():
	em = Enemy()
	all_sprites.add(em)
	enemy.add(em)

def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (pct / 400) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		sub_img = os.path.join(img_folder,'P1.png',)
		self.image = pygame.image.load(sub_img)#.convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 31
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.shield = 400


		self.speedx = 0
		self.speedy = 0

	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -6

		if keystate[pygame.K_RIGHT]:
			self.speedx = 6
		
		if keystate[pygame.K_UP]:
			self.speedy = -3

		if keystate[pygame.K_DOWN]:
			self.speedy = 3


		self.rect.x += self.speedx
		self.rect.y += self.speedy

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH

		if self.rect.left < 0:
			self.rect.left = 0 

		if self.rect.top < 190:
			self.rect.top = 190 

		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT


		#print(self.rect.centerx)
#
	

#####################################################
class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		sub_img = os.path.join(img_folder,'E1.png')
		self.image = pygame.image.load(sub_img).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width *.90 / 2)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,5)

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,5)








		#self.rect.centerx = WIDTH / 2
		#self.rect.bottom = HEIGHT - 1


class SCOREC(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((800,1))
		#sub_img = os.path.join(img_folder,'submarine.png')

		#self.image = pygame.image.load(sub_img).convert()
		self.image.set_colorkey(BLACK)
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT + 1

		

	def update(self):
		self.speedx = 0
		
def show_go_screen():
	screen.blit(blackground, blackground_rect)
	draw_text(screen, "SPACE ESC??", 64, WIDTH / 2, HEIGHT / 4)
	draw_text(screen, "Arrow keys move", 22, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False



#bg
blackground = pygame.image.load(os.path.join(img_folder,'BG1.png')).convert()
blackground_rect = blackground.get_rect()
# sprite is a player
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

enemy = pygame.sprite.Group()
scorec = pygame.sprite.Group()



scorec = SCOREC()
all_sprites.add(scorec)

for i in range(9):
	newene()

#########################################
score = 0
scorereal = score
plus = 1
running = True



#endgame
game_over = True



while running:
#GAME LOOP



	
	clock.tick(FPS)

	for event in pygame.event.get():
		#check for closing
		if event.type == pygame.QUIT:
			running = False
		

	all_sprites.update()

	#enemypass_Check and del
	#hits = pygame.sprite.groupcollide(enemy, scorec, True)
	hits = pygame.sprite.spritecollide(scorec, enemy, True)
	for hit in hits:
		score += 1 
		newene()

#for i in range(1):
#	em = Enemy()
#	all_sprites.add(em)
#	enemy.add(em)






	#playerhitenemy_Check
	hits = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
	for hit in hits:
		player.shield -= hit.radius * 2
		newene()
		if player.shield <= 0:
			game_over = True


	if game_over:
		print(f' Your SCORE IS {score} ')
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		enemy = pygame.sprite.Group()
		scorec = pygame.sprite.Group()
		scorec = SCOREC()
		all_sprites.add(scorec)
		

		for i in range(9):
			newene()
		score = 0
		scorereal = score
		plus = 1
		running = True


	screen.fill(GREY)
	screen.blit(blackground, blackground_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 45, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	pygame.display.flip()




pygame.quit()