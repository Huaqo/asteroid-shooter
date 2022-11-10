# modules
import pygame
import sys
from random import randint, uniform


# functions
def laser_update(laser_list, speed=300):
    for rect in laser_list:
        rect.y -= speed * dt
    # if rect.bottom < 0:
    # 	laser_list.remove(rect)


def meteor_update(meteor_list, speed=300):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * dt
        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)


def display_score():
    score_text = f"Score:{pygame.time.get_ticks() // 1000}"
    text_surf = font.render(score_text, True, "white")
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width=8, border_radius=5)


def laser_timer(can_shoot, duration=500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot


# game init
pygame.init()
clock = pygame.time.Clock()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid Shooter")

# background
background_surf = pygame.image.load("background.png").convert_alpha()

# text
font = pygame.font.Font("subatomic.ttf", 50)

# ship
ship_surf = pygame.image.load("ship.png").convert_alpha()
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser
laser_surf = pygame.image.load("laser.png").convert_alpha()
laser_list = []

# laser timer
can_shoot = True
shoot_time = None

# meteor
meteor_surf = pygame.image.load("meteor.png").convert_alpha()
meteor_list = []

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# import sound
laser_sound = pygame.mixer.Sound("laser.ogg")
expl_sound = pygame.mixer.Sound("explosion.wav")
music_sound = pygame.mixer.Sound("music.wav")
music_sound.play(loops=-1)

# Game Loop
while True:
    # Framerate limit
    dt = clock.tick(120) / 1000

    # Sys Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            # laser
            laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
            laser_list.append(laser_rect)

            # timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # play laser sound
            laser_sound.play()

        if event.type == meteor_timer:
            x_pos = randint(-100, WINDOW_WIDTH + 100)
            y_pos = randint(-100, -50)
            meteor_rect = meteor_surf.get_rect(center=(x_pos, y_pos))
            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
            meteor_list.append((meteor_rect, direction))

    # Control Input
    pygame.mouse.set_visible(False)
    ship_rect.center = pygame.mouse.get_pos()
    pygame.mouse.get_pressed()

    # drawing
    display_surface.blit(background_surf, (0, 0))
    display_score()
    display_surface.blit(ship_surf, ship_rect)

    for rect in laser_list:
        display_surface.blit(laser_surf, rect)

    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    # update
    laser_update(laser_list)
    meteor_update(meteor_list)
    can_shoot = laser_timer(can_shoot, 400)

    # meteor-ship collisions
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        # if ship_rect.colliderect(meteor_rect):
        #   pygame.quit()
        #  sys.exit()

    # laser-meteor collisions
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            if laser_rect.colliderect(meteor_tuple[0]):
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)
                expl_sound.play()

    # final frame
    pygame.display.update()
