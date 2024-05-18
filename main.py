"""
Daniel & Everett
ICS201-02
January 18, 2023
"""
# importing pre-requisites
import pygame
import random
from math import sqrt, pow

# initializing pygame
pygame.init()

# Create colours and variables
black = (41, 41, 40)
white = (255, 255, 255)
orange = (250, 163, 2)
blue = (0, 192, 255)
size = [850, 630] 

# assigning the screen size to variable
screen = pygame.display.set_mode(size)

# For setting window title
pygame.display.set_caption("Rocket Joyride")

# Spaceship initial x and y values
x_spaceship = 200
y_spaceship = 150

# Ground and obstacle scrolling initial values along with scroll speed.
ground_scroll = 0
obstacle_scroll = 1200
scroll_speed = 4

# height offset which sets a random value between 0 and 100
height_offset = random.randint(0, 100)

# Initial Booleans for game over, hard mode, and menu
game_over = True 
hardmode = False
menu = True

# random value for y axis
y_random = random.randint(100, 200)

# load the spaceship image to memory and scaling it to the following
spaceship = pygame.image.load('spaceship.png')
resized_spaceship = pygame.transform.scale(spaceship, (60,60))
roatated_spaceship = pygame.transform.rotate(resized_spaceship, -90)

# Loading the mountain image and scaling it to the following
mountain_top = pygame.image.load('mountains.png')
resized_mountain = pygame.transform.scale(mountain_top, (1500, 700))

# Load the Rocket Joyride logo and scaling it to the following
logo = pygame.image.load('logo.png')
logo_scaled = pygame.transform.scale(logo, (500, 100))

# loading the diamond collectible image
diamond_collectible = pygame.image.load('diamond.png')

# Setting the ground coordinates and filling it with the color blue
ground = pygame.Surface([1000, 400])
ground.fill(blue)

# Mountain collider which has 0 opacity and rotated.
mountain_collider = pygame.Surface([250, 280])
mountain_collider.set_alpha(0) 
rotated_mountain_collider = pygame.transform.rotate(mountain_collider, 95)

# Clock 
clock = pygame.time.Clock()

# Initial values for lives and score
# Lives for second chance. Score to set the score
lives = 2
score = 0

# fonts in different sizes
font1 = pygame.font.Font("Pixeboy.ttf", 50)
font2 = pygame.font.Font("Pixeboy.ttf", 30)

# Passthrough game object which has 0 opacity
passThrough = pygame.Surface([20, 250])
passThrough.set_alpha(0)

# Buttons for the menu
Easy_button = pygame.draw.rect(screen, black, [363, 365, 100, 20])
Hard_button = pygame.draw.rect(screen, black, [363, 405, 100, 20])
Quit_button = pygame.draw.rect(screen, black, [393, 445, 100, 20])

# Initial rotation speed
rotation_Speed = 0

# passing through function for the passThrough game object which has x and y in the paramater. 
def passingThrough(x, y):
  screen.blit(passThrough, [obstacle_scroll + x, height_offset + y])

# mountain function for creating an invisible game object on the mountain image. 
def mountain(x = 0, y = 0):
  screen.blit(mountain_collider, [obstacle_scroll + x, height_offset + y])

# Collision detection function 
def isCollision(x1, y1, x2, y2):
  distance  = sqrt((pow(x1 - x2, 2)) + (pow(y1 - y2, 2)))
  if distance < 27:
    return True
  else:
    return False

done = False

# Obstacle function for spawning the mountain, and the invisible game object
def Obstacle():
    screen.blit(resized_mountain, [obstacle_scroll, -height_offset])
    mountain(150, -150)
    mountain(230, 400)
    mountain(600, -200)
    mountain(1200, -90)
    mountain(1200, 380)
    mountain(680, 260)
    passingThrough(310, 200)
    passingThrough(740, 80)
    passingThrough(1240, 200)
# Function when game_over is false
def Game():
    # globalizing all the variables since it's inside a function
    global x_spaceship, y_spaceship, score, ground_scroll, obstacle_scroll, height_offset, game_over
      # creating a variable for when keys are pressed
    keys = pygame.key.get_pressed()

    # Condition if the space key is pressed
    if keys[pygame.K_SPACE]:
      y_spaceship -= 5
    else:
      y_spaceship += 7
      if y_spaceship >= 500:
        explosion_sfx = pygame.mixer.Sound("game_over.wav")
        explosion_sfx.play()
        game_over = True

    screen.fill(black) 
    
    # Texts rendering in the top and top right corner
    scoreImage = font1.render(f"{score}", True, white)
    livesImage = font2.render(f"Lives: {lives}", True, white)

    # spaceship, ground, obstacle, and collectible with the following variables set as their x and y axis
    screen.blit(roatated_spaceship, [x_spaceship, y_spaceship]) 
    screen.blit(ground, [ground_scroll, 550])
    screen.blit(diamond_collectible, (obstacle_scroll, y_random))
    Obstacle()
    
    # Conditions if obstacle scroll is less than or equal to -1500
    if obstacle_scroll <= -1500:
      obstacle_scroll = 800
      height_offset = random.randint(50, 100)
      diamond_collectible.set_alpha(255)
    # Conditions if the absolute value of ground_scroll is more than or equal to 35
    if abs(ground_scroll) >= 35:
      ground_scroll = 0
    
    # Obstacle and ground scroll deducting as they immitate the spaceship movement
    obstacle_scroll -= scroll_speed - 1
    ground_scroll -= scroll_speed

    # collisions for when the spaceship passes through an obstacle
    collision1 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 310, height_offset + 300)
    collision2 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 740, height_offset + 200)
    collision3 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 1240, height_offset + 300)

    # collisions for when the spaceship hits an obstacle
    mountain_collision1 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 150, height_offset + -150)
    mountain_collision2 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 100, height_offset + 410)
    mountain_collision3 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 600, height_offset + -200)
    mountain_collision4 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 1200, height_offset + -90)
    mountain_collision5 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 1200, height_offset + 380)
    mountain_collision6 = isCollision(x_spaceship, y_spaceship, obstacle_scroll + 680, height_offset + 250)

    # collision for when the spaceship has collided with the diamond collectible
    diamond_collision = isCollision(x_spaceship, y_spaceship, obstacle_scroll, y_random)

    # Conditions if the spaceship has collided with the diamond
    if diamond_collision:
      diamond_collectible.set_alpha(0)
      ching_sfx = pygame.mixer.Sound("collecting.wav")
      ching_sfx.play()
      score += 1
    # Conditions if the spaceship has collided with the mountains
    if mountain_collision1 or mountain_collision2 or mountain_collision3 or mountain_collision4 or mountain_collision5 or mountain_collision6:
      game_over = True
      explosion_sfx = pygame.mixer.Sound("game_over.wav")
      explosion_sfx.play()
    # Conditions for when the spaceship passes through an obstacle
    if collision1:
      score += 1
    elif collision2:
      score += 2
    elif collision3:
      score += 3
    # rendering the score and lives text to the following coordinates
    screen.blit(scoreImage, (450, 10))
    screen.blit(livesImage, (750, 10))
# function for showing the game menu
def Menu():
    screen.fill(black)
    screen.blit(logo_scaled, (180, 185))
    screen.blit(EasyMode, (363, 365))
    screen.blit(HardMode, (363, 405))
    screen.blit(quit, (393, 445))
# Function to show the gameOver screen when life is less than 2
def GameOver():

    global EasyMode, HardMode, quit, restart_button, menu
    screen.fill(orange)
    # Render the font for easy mode, hard mode, and quit
    EasyMode = font2.render("Easy Mode", True, white)
    HardMode = font2.render("Hard Mode", True, white)
    quit = font2.render("Quit", True, white)
    # Conditions if lives is set to 1
    if lives - 1 == 1:
      # Rendering the game over text, the amount of lives left, and the restart button
      gameOverImage = font1.render("Game Over", True, white)
      livesImage = font2.render(f"You have {lives - 1} life left", True, white)
      restart_button = pygame.draw.rect(screen, orange, [376, 415, 100, 50])
      restartImage = font2.render("Restart", True, white)
      screen.blit(restartImage, (376, 415))
      screen.blit(gameOverImage, (333, 250))
      screen.blit(livesImage, (313, 450))
    else:
      # show the menu
      menu = True

# While the program is running
while not done:
  # add .5 to rotation speed so that the screen rotates based on the following speed
  rotation_Speed += .5

  # clock ticking at 110
  clock.tick(110)

  # events that occur in the game such as: when the program quits, and when the following buttons are clicked
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    # the following code is for when you click on the following buttons
    if event.type == pygame.MOUSEBUTTONDOWN:
      # if you click on the restart button, the variables will be set to the following
      if restart_button.collidepoint(event.pos) and game_over == True:
        game_over = False
        lives = 1
        x_spaceship = 200
        y_spaceship = 150
        ground_scroll = 0
        obstacle_scroll = 1200
      # if you click on the easy mode button, the variables will be set to the following
      if Easy_button.collidepoint(event.pos) and menu == True:
        menu = False
        game_over = False
        hardmode = False
        lives = 2
        x_spaceship = 200
        y_spaceship = 150
        ground_scroll = 0
        obstacle_scroll = 1200
        score = 0
      # if you click on the hard mode button, the variables will be set to the following
      if Hard_button.collidepoint(event.pos) and menu == True:
        menu = False
        game_over = False
        hardmode = True
        lives = 1
        x_spaceship = 200
        y_spaceship = 150
        ground_scroll = 0
        obstacle_scroll = 1200 
        score = 0
      # if you click on the quit button, it would break the loop and quit
      if Quit_button.collidepoint(event.pos) and menu == True:
        done = True
  # Conditions if game_over is True     
  if game_over == True:
    # Evoke the GameOver() function
    GameOver()
    # Conditions for showing a menu 
  if menu == True:
    # Evoke the Menu() function
    Menu()
    
  elif game_over == False:
    # evoke the Game() function
    Game()
    # Conditions when hard mode is set to True
    if hardmode == True:
      screen.blit(pygame.transform.rotate(screen, rotation_Speed ), (0, 0))
    else:
      screen.blit(pygame.transform.rotate(screen, 0), (0, 0))
  pygame.display.flip()

pygame.quit()
# references
# https://www.pygame.org/docs/ref/surface.html
# https://www.pygame.org/docs/ref/transform.html
# https://www.pygame.org/docs/ref/key.html
