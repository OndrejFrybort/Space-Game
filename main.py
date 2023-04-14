import pygame
import time
import random
from pygame import mixer
pygame.font.init()

#Constants
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("media/bg.jpg")
PLAYER_VEL = 5
FONT = pygame.font.SysFont("Arial", 30)
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

#Image
player = pygame.image.load("media/ship.png")
player_rect = player.get_rect()
player_rect.center = WIDTH/2, HEIGHT - 30

point = pygame.image.load ("media/point.png")
point_rect = point.get_rect()
point_rect.center = (WIDTH//2, HEIGHT//2)

#Window setting
pygame.display.set_caption("Space Game")
pygame_icon = pygame.image.load('media/icon.png')
pygame.display.set_icon(pygame_icon)

#Music
mixer.init()
pygame.mixer.music.load("media/bg.wav")
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(0.1)

loose_life_sound = pygame.mixer.Sound("media/boom.wav")
loose_life_sound.set_volume(0.1)
take_point_sound = pygame.mixer.Sound("media/point.wav")
take_point_sound.set_volume(0.1)

#Draw
def draw(player, elapsed_time, stars, score):
    WIN.blit(BG,(0,0))
    WIN.blit(player, player_rect)
    WIN.blit(point, point_rect)
    score_text = FONT.render(f"Score: {round(score)}", 1, "white")
    WIN.blit(score_text, (10, 10))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 40))

    for star in stars:
        pygame.draw.rect (WIN, "white", star)

    pygame.display.update()

#Main loop
def main():
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    score = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time()-start_time
        #Star generator
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left - PLAYER_VEL>=0:
            player_rect.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player_rect.right + PLAYER_VEL <=WIDTH:
            player_rect.x += PLAYER_VEL
        elif keys[pygame.K_DOWN] and player_rect.bottom + PLAYER_VEL<=HEIGHT:
            player_rect.y += PLAYER_VEL
        elif keys[pygame.K_UP] and player_rect.top - PLAYER_VEL >=0:
            player_rect.y -= PLAYER_VEL
        #Stars collision
        for star in stars [:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player_rect.top and star.colliderect(player_rect):
                stars.remove(star)
                hit = True
                break
        #Point generator
        if point_rect.colliderect(player_rect):
            point_rect.centerx = random.randint(0, WIDTH)
            point_rect.centery = random.randint(50, HEIGHT)
            score = score + 1
            take_point_sound.play()
        #
        if hit:
            lost_text = FONT.render("You lost", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            loose_life_sound.play()
            pygame.display.update()
            pygame.time.delay(4000)
            break     
        
        draw(player, elapsed_time, stars, score)
    pygame.quit()

if __name__ == "__main__":
    main()