# Hi I'm Ajay 
# Thanks for downloading source code from Github.com
# :)
# Importing Modules
import pygame
import os
# Initiaitiong PyGame font
pygame.font.init()
# Initiaitiong PyGame Mixer for BGM
pygame.mixer.init()
# Change Application Title Name
pygame.display.set_caption("Planetary Wars")
# Constants
#----Dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)
#----New Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
#----Colors
RED_BULLET_COLOR = (255,0,0)
YELLOW_BULLET_COLOR = (255,255,0)
FONT_COLOR = (255,255,255)
BORDER_COLOR = (0,0,0)
#----I don't know how to name it
BULLET_VEL = 7
FPS = 60
VEL = 5
MAX_BULLETS = 5
#---Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)
#---Audios
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
#---Images
YELLOW_SPACEPSHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACEPSHP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACEPSHIP_IMAGE,(55,40)), 270)
RED_SPACEPSHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACEPSHP = pygame.transform.rotate(pygame.transform.scale(RED_SPACEPSHIP_IMAGE, (55,40)), 90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH, HEIGHT))
# Functions
def draw_function(red , yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
    red_health_text = HEALTH_FONT.render(f'Health: {red_health}', 1, FONT_COLOR)
    yellow_health_text = HEALTH_FONT.render(f'Health: {yellow_health}', 1, FONT_COLOR)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACEPSHP ,(yellow.x, yellow.y))
    WIN.blit(RED_SPACEPSHP ,(red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_BULLET_COLOR, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_BULLET_COLOR, bullet)
    pygame.display.update()
def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    elif key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15:
        yellow.x += VEL
    elif key_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    elif key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL
def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    elif key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15:
        red.x += VEL
    elif key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    elif key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, FONT_COLOR)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
def main():
    red = pygame.Rect(700, 300, 55,40)
    yellow = pygame.Rect(100, 300, 55,40)
    clock = pygame.time.Clock()
    run = True
    red_health = 10
    yellow_health = 10
    red_bullets = []
    yellow_bullets = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Hurrah! Left Wins!"
        if yellow_health <= 0:
            winner_text = "Congrats! Right Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_function(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()
# Calling Main Function
if __name__ == '__main__':
    main()
