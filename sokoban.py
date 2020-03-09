# Name: pySokoban
# Description: A sokoban implementation using python & pyGame
# Author: Kazantzakis Nikos <kazantzakisnikos@gmail.com>
# Date: 2015
# Last Modified: 31-03-2016

import pygame
import datetime
import os
import time
import sys
from Environment import Environment
from Level import Level, NonexistentLevelException

def drawLevel(matrix_to_draw):
	
	# Load level images
	wall = pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/wall.png').convert()
	box = pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/box.png').convert()
	box_on_target =  pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/box_on_target.png').convert()
	space = pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/space.png').convert()
	target = pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/target.png').convert()
	player = pygame.image.load(myEnvironment.getPath() + '/themes/' + theme + '/images/player.png').convert()
	
	# If horizontal or vertical resolution is not enough to fit the level images then resize images
	if myLevel.getSize()[0] > myEnvironment.size[0] / 36 or myLevel.getSize()[1] > myEnvironment.size[1] / 36:
		
		# If level's x size > level's y size then resize according to x axis
		if myLevel.getSize()[0] / myLevel.getSize()[1] >= 1:
			new_image_size = myEnvironment.size[0]/myLevel.getSize()[0]
		# If level's y size > level's x size then resize according to y axis
		else:
			new_image_size = myEnvironment.size[1]/myLevel.getSize()[1]
		
		# Just to the resize job	
		wall = pygame.transform.scale(wall, (new_image_size,new_image_size))
		box = pygame.transform.scale(box, (new_image_size,new_image_size))
		box_on_target = pygame.transform.scale(box_on_target, (new_image_size,new_image_size))
		space = pygame.transform.scale(space, (new_image_size,new_image_size))
		target = pygame.transform.scale(target, (new_image_size,new_image_size))
		player = pygame.transform.scale(player, (new_image_size,new_image_size))	
		
	# Just a Dictionary (associative array in pyhton's lingua) to map images to characters used in level design 
	images = {'#': wall, ' ': space, '$': box, '.': target, '@': player, '*': box_on_target}
	
	# Get image size. Images are always squares so it doesn't care if you get width or height
	box_size = wall.get_width()
	
	# Iterate all Rows
	for i in range (0,len(matrix_to_draw)):
		# Iterate all columns of the row
		for c in range (0,len(matrix_to_draw[i])):
			myEnvironment.screen.blit(images[matrix_to_draw[i][c]], (c*box_size, i*box_size))

	pygame.display.update()
				
def movePlayer(direction,myLevel):
	
	matrix = myLevel.getMatrix()
	
	myLevel.addToHistory(matrix)
	
	x = myLevel.getPlayerPosition()[0]
	y = myLevel.getPlayerPosition()[1]
	
	global target_found
	
	if direction == "L":
		# if is_space
		if matrix[y][x-1] == " ":
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x-1] == "$":
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
				
				
		# if is_box_on_target
		elif matrix[y][x-1] == "*":
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
		# if is_target
		elif matrix[y][x-1] == ".":
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
	
	elif direction == "R":
		# if is_space
		if matrix[y][x+1] == " ":
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x+1] == "$":
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "				
		
		# if is_box_on_target
		elif matrix[y][x+1] == "*":
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
			
		# if is_target
		elif matrix[y][x+1] == ".":
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True

	elif direction == "D":
		# if is_space
		if matrix[y+1][x] == " ":
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y+1][x] == "$":
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
		
		# if is_box_on_target
		elif matrix[y+1][x] == "*":
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
		
		# if is_target
		elif matrix[y+1][x] == ".":
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True

	elif direction == "U":
		# if is_space
		if matrix[y-1][x] == " ":
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y-1][x] == "$":
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "

			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "					
					
		# if is_box_on_target
		elif matrix[y-1][x] == "*":
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
					
		# if is_target
		elif matrix[y-1][x] == ".":
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
	drawLevel(matrix)
	
	if len(myLevel.getBoxes()) == 0:
		myEnvironment.screen.fill((0, 0, 0))
		global current_level
		print_score(current_level)
		current_level += 1
		initLevel(level_set,current_level)	

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_score(level):
	global start_time
	elapsed_time = datetime.timedelta(seconds=time.time() - start_time)
	total_seconds = int(elapsed_time.total_seconds())
	hours, remainder = divmod(total_seconds,60*60)
	minutes, seconds = divmod(remainder,60)

	print "Best time for level {lvl}: {bold}4 hours 27 minutes 31 seconds{end}".format(
		lvl=level, bold=color.GREEN+color.BOLD, end=color.END,
	)
	print "Your time for level {lvl}: {bold}{h} hours {m} minutes {s} seconds{end}".format(
		lvl=level, bold=color.GREEN+color.BOLD, h=hours, m=minutes, s=seconds, end=color.END,
	)

class Error483(Exception):
	def __init__(self, msg):
		super(Error483, self).__init__(color.RED + color.BOLD + msg + color.END)

def print_traceback():
	raise Error483("Error 483")

with open(os.path.dirname(os.path.abspath(__file__)) + '/easter_egg', 'r') as f:
    easter_egg_sequence = f.read().splitlines()[0]

history = ""

def check_easter_egg(direction):
    global history
    global easter_egg_sequence
    history += direction
    history = history[-len(easter_egg_sequence):]
    if history == easter_egg_sequence:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/winning-message.txt', 'r') as f:
            print f.read()
        print "Time: %s" % datetime.datetime.now().time()
        pygame.quit()
        sys.exit()

def initLevel(level_set,level):
	# Create an instance of this Level
	global myLevel
	try:
		myLevel = Level(level_set,level)
	except NonexistentLevelException:
		pygame.quit()
		sys.exit()

	# Draw this level
	drawLevel(myLevel.getMatrix())
	
	global target_found
	target_found = False
	

# Create the environment
myEnvironment = Environment()

# Choose a theme
theme = "default"

# Choose a level set
level_set = "exit_game_2020"

# Set the start Level
current_level = 1

# Initialize Level
initLevel(level_set,current_level)
start_time = time.time()

target_found = False

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				movePlayer("L",myLevel)
				check_easter_egg("<")
			elif event.key == pygame.K_RIGHT:
				movePlayer("R",myLevel)
				check_easter_egg(">")
			elif event.key == pygame.K_DOWN:
				movePlayer("D",myLevel)
				check_easter_egg("_")
			elif event.key == pygame.K_UP:
				movePlayer("U",myLevel)
				check_easter_egg("^")
			elif event.key == pygame.K_u:
				drawLevel(myLevel.getLastMatrix())
			elif event.key == pygame.K_r:
				initLevel(level_set,current_level)
			elif event.key == pygame.K_ESCAPE:
				print_traceback()
				pygame.quit()
				sys.exit()
			if event.unicode.isalnum():
				check_easter_egg(event.unicode)
		elif event.type == pygame.QUIT:
			print_traceback()
			pygame.quit()
			sys.exit()
	else:
		elapsed_time = datetime.timedelta(seconds=time.time() - start_time)
		if elapsed_time >= datetime.timedelta(minutes=10):
			print_traceback()
			pygame.quit()
			sys.exit()

