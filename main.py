import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((900, 500))

# Background
background = pygame.image.load('output-onlinepngtools (2).png')

# Background Sound
mixer.music.load('Kevin MacLeod - 8bit Dungeon Level NO COPYRIGHT 8-bit Music.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Kosmos İşgalçıları")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('output-onlinepngtools.png')
playerX = 400
playerY = 400
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 835))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

# Bullet
# You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# blit = draw
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False


def show_score(x, y):
    score = font.render("Score : {}".format(str(score_value)), True, (52, 61, 82))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("Game Over", True, (1, 1, 1))
    screen.blit(over_text, (270, 200))


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        # KEYDOWN - pressing any button on the keyboard
        # KEYUP - releasing that press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser-gun-19sf.mp3')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    # Enemy movement
    for i in range(number_of_enemies):

        # Game Over
        #if enemyY[i] > 200:
        #    for j in range(number_of_enemies):
         #       enemyY[j] = 2000
        #    game_over()
         #   break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('Explosion+1.mp3')
            explosion_Sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 835)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # After every change in the display, it is necessary to update the display in the game loop.
    pygame.display.update()
