import pygame, sys
from pygame import mixer
from levels.levels import *
from os import path

#list of levels
niveaux = [level_data1, level_data2, level_data3, level_data4, level_data5]

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#define game variables
tile_size = 50
game_over = 0
main_menu = True
in_options = False
run = True
playing = False
in_credit = False
in_skin = False
score = 0
level = 0
max_levels = len(niveaux)

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#sun_img = pygame.image.load('img/LV3.png')
bg_img = pygame.image.load('img/background.jpg')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
option_img = pygame.image.load('img/option.png')
credit_img = pygame.image.load('img/credit.png')
spike_img = pygame.image.load('img/spike.png')
runstickman_img = pygame.image.load('img/runstickman.png')
skin_img = pygame.image.load('img/skin.png')
skin1_img = pygame.image.load('img/skin1-1.png')
skin2_img = pygame.image.load('img/skin2-1.png')
skin3_img = pygame.image.load('img/skin3-1.png')
creator_img = pygame.image.load('img/creator.png')
creator2_img = pygame.image.load('img/foggy.png')
nom_img = pygame.image.load('img/nom.png')

#function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	fire_group = pygame.sprite.Group()
	coin_group = pygame.sprite.Group()
	exit_group = pygame.sprite.Group()
	
	world = World(niveaux[level])
	player.reset(100, screen_height - 650)
	return world

#load sound
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('img/img_jump.wav')
jump_fx.set_volume(0.3)
game_over_fx = pygame.mixer.Sound('img/img_game_over.wav')
game_over_fx.set_volume(0.3)
coin_fx = pygame.mixer.Sound('img/coin.mp3')
game_over_fx.set_volume(0.2)
xp_fx = pygame.mixer.Sound('img/xp.wav')

#def draw_grid():
	#for line in range(0, 40):
		#pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		#pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))




def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action

#player create

class Player():
	skin = "skin1"
	def __init__(self, x, y):
		self.reset(x, y)

	def set_skin(self, skin):
		xp_fx.play()
		self.skin = skin


	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 1

		if game_over == 0 :
			# get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False :
				jump_fx.play()
				self.vel_y = -14
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			if key[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()






			# handle animation
			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			#if self.vel_y > 10:
				#self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			#check for collision with enemies
			if pygame.sprite.spritecollide(self, fire_group, False):
				game_over = -1
				game_over_fx.play()
				pygame.mixer.music.stop()

			# check for collision with enemies
			if pygame.sprite.spritecollide(self, spike_group, False):
				game_over = -1
				game_over_fx.play()
				pygame.mixer.music.stop()

			# check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 3)
			if self.rect.y > 200:
				self.rect.y -= 5


		#draw player onto screen
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		return game_over

		#dessin le joueur sur l'écran
		screen.blit(self.image, self.rect)


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 9):
			img_right = pygame.image.load(f'img/{self.skin}-{num}.png')
			img_right = pygame.transform.scale(img_right, (60, 80 ))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True


class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		cube_img = pygame.image.load('img/ROUGE.png')
		#grass_img = pygame.image.load('img/grass.png')
		coin_img = pygame.image.load('img/coin.png')

		self.enemyList = []
		self.spikeList = []

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(cube_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					fire = Enemy(col_count * tile_size, row_count * tile_size + 15)
					self.enemyList.append(fire)
					fire_group.add(fire)
					col_count += 1
				if tile == 3:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 4:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				if tile == 5:
					spike = Spike(col_count * tile_size+ 23, row_count * tile_size +25)
					spike_group.add(spike)
					self.spikeList.append(spike)



				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 100:
			self.move_direction *= -1
			self.move_counter = 0

	def __del__(self):
		return

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Spike(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/spike.png')
		self.image = pygame.transform.scale(img, (tile_size , tile_size ))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

player = Player(100, screen_height - 500)
fire_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
runstickman_group = pygame.sprite.Group()

#load in level data and create world

#world_data = level_data1
world = World(niveaux[0])


# create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + -100, restart_img)
start_button = Button(screen_width // 2 - 20, screen_height // 2 + -105, start_img)
exit_button = Button(screen_width // 2 - 350, screen_height // 2 + -105, exit_img)
option_button = Button(screen_width // 1 - 1150, screen_height // 2 + 70, option_img)
credit_button = Button(screen_width // 1 - 1150, screen_height // 2 + 200, credit_img)
runstickman_button = Button(screen_width // 1 - 1920, screen_height // 2 + -550, runstickman_img)
skin_button = Button(screen_width // 2 - 150, screen_height // 2 + -80, skin_img)
exit_button2 = Button(screen_width // 2 - 980, screen_height // 1 + -105, exit_img)
skin1_button = Button(screen_width // 1 - 1700, screen_height // 2 + -180, skin1_img)
skin2_button = Button(screen_width // 1 - 1300, screen_height // 2 + -300, skin2_img)
skin3_button = Button(screen_width // 1 - 800, screen_height // 2 + -300, skin3_img)
creator_button = Button(screen_width // 1 - 1380, screen_height // 2 + -500, creator_img)
creator2_button = Button(screen_width // 1 -1450, screen_height // 2 + -200, creator2_img)
nom_button = Button(screen_width // 1 -1120, screen_height // 2 + -150, nom_img)
while run:

	clock.tick(fps)
	screen.blit(bg_img, (0, 0))



	if main_menu == True :

		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
			playing = True
			xp_fx.play()
		if option_button.draw():
			main_menu = False
			in_options = True
		if credit_button.draw():
			main_menu = False
			in_credit = True


		runstickman_button.draw()
		credit_button.draw()

	if in_options == True:
		# Options menu
		screen.blit(bg_img, (0,0))
		runstickman_button.draw()


		if skin_button.draw():
			# skin menu

			in_options = False
			in_skin = True
		if exit_button2.draw():
			main_menu = True
			in_options = False

	if in_credit == True:
		runstickman_button.draw()
		creator_button.draw()
		creator2_button.draw()
		nom_button.draw()

		if exit_button2.draw():
			main_menu = True
			in_options = False
			in_skin = False
			in_credit = False




	if in_skin == True :

		runstickman_button.draw()
		if skin1_button.draw():	
			player.set_skin("skin1")
			player.reset(100, screen_height - 650)


		if skin2_button.draw():
			player.set_skin("skin2")
			player.reset(100, screen_height - 650)


		if skin3_button.draw():
			player.set_skin("skin3")
			player.reset(100, screen_height - 650)



		if exit_button2.draw():
			main_menu = True
			in_options = False
			in_skin = False












	elif playing == True:
		world.draw()

		if game_over == 0:
			player.skin = "skin2"
			fire_group.update()
			# update score
			# check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

		fire_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		spike_group.draw(screen)


		# create dummy coin for showing the score
		score_coin = Coin(tile_size // 2, tile_size // 2)
		coin_group.add(score_coin)


		game_over = player.update(game_over)

		# if player has died
		if game_over == -1:
			if restart_button.draw():
				xp_fx.play()
				player.reset(100, screen_height - 650)
				game_over = 0
				pygame.mixer.music.play()

		# if player has completed the level
		if game_over == 1:
			# reset game and go to next level
			level += 1
			if level < max_levels:
				# reset level
				world_data = []
				for e in world.enemyList:
					fire_group.remove(e)
				spike_group.empty()
				coin_group.empty()
				exit_group.empty()
				score = 0
				


				world = reset_level(level)
				game_over = 0
			else:
				if restart_button.draw():
					level = 0
					# reset level
					world_data = []
					world = reset_level(level)
					game_over = 0



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
