import pygame
import random
import math
from pygame import mixer

# pygame setup
x = pygame.init()
FPS = 60

game_window = pygame.display.set_mode((800, 600))

#Game Title
pygame.display.set_caption("Space Invader")

#Logo Image
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

#Background Image
background = pygame.image.load("images/background.png")

#Background Music
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

#Bullet fire music
bullet_sound = mixer.Sound("sounds/laser.wav")

#Collision sound
collide_sound = mixer.Sound("sounds/explosion.wav")

#Flags
running = True
key_action_allowed = True

#Player
player_image = pygame.image.load("images/arcade-game.png")
playerX = 370
playerY = 500
X_change = 0
Y_change = 0

#Creating 5 Enemies
enemy_image = []
enemyX = []
enemyY = []
num_of_enemies = 5
enemy_x_change = []
enemy_y_change = []

for i in range(num_of_enemies):
    resize_enemy = pygame.transform.scale(pygame.image.load("images/monster.png"), (50, 50))
    enemy_image.append(resize_enemy)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemy_x_change.append(8)
    enemy_y_change.append(35)

#Bullet Firing
bullet_image = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 500
bullet_x_change = 0
bullet_y_change = 20
bullet_state = "ready"

#Score
score = 0
font = pygame.font.Font("fonts/Lazy Monday.otf", 32)

#Game Over text
over_text = pygame.font.Font("fonts/Lazy Monday.otf", 64)
score_text = pygame.font.Font("fonts/Lazy Monday.otf", 50)

def show_score(x, y):
    score_text = font.render("Score : " + str(score), True, (255, 255, 255))  # Render the score text
    game_window.blit(score_text, (x, y))

def game_over():
    global bullet_state, key_action_allowed
    game_over_text = over_text.render("GAME OVER!", True, (255, 255, 255))
    final_score_text = score_text.render(f"Your Final Score: {score}", True, (255, 255, 255))
    game_window.blit(game_over_text, (240, 220))
    game_window.blit(final_score_text, (210, 300))
    mixer.music.stop()
    bullet_sound.stop()
    bullet_state = "ready"
    key_action_allowed = False

def isCollide(bullet_x, enemy_x, bullet_y, enemy_y):
    distance = math.sqrt((bullet_x - enemy_x)**2 + (bullet_y - enemy_y)** 2)
    if distance <= 27:
        return True
    else:
        return False

def image_load(x, y):
    game_window.blit(player_image, (x, y))

def enemy_load(x, y, num):
    game_window.blit(enemy_image[num], (x, y))

def fire_bullet(x, y):
    global bullet_state
    game_window.blit(bullet_image, (x+16, y+10))
    bullet_state = "fired"

clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    game_window.fill((7, 9, 9))
    game_window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if key_action_allowed:
                if event.key == pygame.K_RIGHT:
                    X_change = 15
                if event.key == pygame.K_LEFT:
                    X_change = -15
                # if event.key == pygame.K_UP:
                #     Y_change = -15
                # if event.key == pygame.K_DOWN:
                #     Y_change = 15
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                X_change = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     Y_change = 0

    #Player Movement
    playerX += X_change
    playerY += Y_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    # elif playerY > 536:
    #     playerY = 536

    #Enemy Movement
    for num in range(num_of_enemies):
        enemyX[num] += enemy_x_change[num]

        #Game Over
        if enemyY[num] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        if enemyX[num] <= 0:
            enemy_x_change[num] = 8
            enemyY[num] += enemy_y_change[num]
        elif enemyX[num] >= 735:
            enemy_x_change[num] = -8
            enemyY[num] += enemy_y_change[num]

        # Collision Detection
        collision = isCollide(bulletX, enemyX[num], bulletY, enemyY[num])
        if collision:
            collide_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            enemyX[num] = random.randint(0, 735)
            enemyY[num] = random.randint(30, 150)
        enemy_load(enemyX[num], enemyY[num], num)
        show_score(10, 10)

    #Bullet Movement
    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_y_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 500

    image_load(playerX, playerY)
    pygame.display.update()


pygame.quit()
