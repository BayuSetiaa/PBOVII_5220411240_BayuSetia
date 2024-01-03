import sys

import pygame
import random

from controls import move_player, move_player_with_joystick
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from functions import show_game_over, music_background
from menu import show_menu, animate_screen

from classes.srigala import Player
from classes.peluru import Peluru
from classes.refill import BulletRefill, HealthRefill, DoubleRefill, ExtraScore
from classes.peternak import Peternak, Peternak2
from classes.explosions import Explosion, Explosion2
from classes.musuh import Musuh1, Musuh2
from classes.dinosaurus import Dino1, Dino2, Dino3


pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Wolf of Farm")
clock = pygame.time.Clock()


def main():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('game_sounds/menu.mp3')
    pygame.mixer.music.play(-1)
    animate_screen()


explosions = pygame.sprite.Group()
explosions2 = pygame.sprite.Group()
peluru = pygame.sprite.Group()
musuh1_group = pygame.sprite.Group()
musuh2_group = pygame.sprite.Group()
dino1_group = pygame.sprite.Group()
boss2_group = pygame.sprite.Group()
dino3_group = pygame.sprite.Group()
peluru_refill_group = pygame.sprite.Group()
health_refill_group = pygame.sprite.Group()
double_refill_group = pygame.sprite.Group()
orang_group = pygame.sprite.Group()
orang2_group = pygame.sprite.Group()
extra_score_group = pygame.sprite.Group()
musuh2_peluru = pygame.sprite.Group()

dino1_peluru = pygame.sprite.Group()
dino2_peluru = pygame.sprite.Group()
dino3_peluru = pygame.sprite.Group()

dino1_health = 150
dino1_health_bar_rect = pygame.Rect(0, 0, 150, 5)
dino1_spawned = False

dino2_health = 150
dino2_health_bar_rect = pygame.Rect(0, 0, 150, 5)
dino2_spawned = False

dino3_health = 200
dino3_health_bar_rect = pygame.Rect(0, 0, 200, 5)
dino3_spawned = False

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/bg/background.jpg').convert()
background_img2 = pygame.image.load('images/bg/background2.png').convert()
background_img3 = pygame.image.load('images/bg/background3.png').convert()
background_img4 = pygame.image.load('images/bg/background4.png').convert()
background_top = background_img.copy()
current_image = background_img
new_background_activated = False

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(8)]
explosion2_images = [pygame.image.load(f"images/explosion2/explosion{i}.png") for i in range(18)]
explosion3_images = [pygame.image.load(f"images/explosion3/explosion{i}.png") for i in range(18)]

musuh1_img = [
    pygame.image.load('images/musuh_srigala/musuh1_1.png').convert_alpha(),
    pygame.image.load('images/musuh_srigala/musuh1_2.png').convert_alpha(),
    pygame.image.load('images/musuh_srigala/musuh1_3.png').convert_alpha()
]
musuh2_img = [
    pygame.image.load('images/musuh_srigala/musuh2_1.png').convert_alpha(),
    pygame.image.load('images/musuh_srigala/musuh2_2.png').convert_alpha()
]
dino1_img = pygame.image.load('images/dinosaurus/dino1.png').convert_alpha()
dino2_img = pygame.image.load('images/dinosaurus/dino2_1.png').convert_alpha()
dino3_img = pygame.image.load('images/dinosaurus/dino3.png').convert_alpha()

health_refill_img = pygame.image.load('images/refill/health_refill.png').convert_alpha()
peluru_refill_img = pygame.image.load('images/refill/bullet_refill.png').convert_alpha()
double_refill_img = pygame.image.load('images/refill/double_refill.png').convert_alpha()

peternak_imgs = [
    pygame.image.load('images/peternak/orang_1.png').convert_alpha(),
    pygame.image.load('images/peternak/orang_2.png').convert_alpha(),
    pygame.image.load('images/peternak/orang_3.png').convert_alpha(),
    pygame.image.load('images/peternak/orang_4.png').convert_alpha()
]
peternak2_imgs = [
    pygame.image.load('images/peternak/orang2_1.png').convert_alpha(),
    pygame.image.load('images/peternak/orang2_2.png').convert_alpha(),
    pygame.image.load('images/peternak/orang2_3.png').convert_alpha(),
    pygame.image.load('images/peternak/orang2_4.png').convert_alpha()
]
extra_score_img = pygame.image.load('images/sapi/sapi_coin.png').convert_alpha()

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
hi_score = 0
player = Player()
player_life = 10000
bullet_counter = 10000

paused = False
running = True

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

if show_menu:
    import menu
    menu.main()

is_shooting = False
last_shot_time = 0


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                if bullet_counter > 0 and pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                    last_shot_time = pygame.time.get_ticks()
                    bullet = Peluru(player.rect.centerx, player.rect.top)
                    peluru.add(bullet)
                    bullet_counter -= 1
                is_shooting = True

            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
                paused = not paused
            elif not paused:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.original_image is not None:
                player.image = player.original_image.copy()
                is_shooting = False
            elif not paused:
                if event.key == pygame.K_LEFT:
                    player.stop_left()
                elif event.key == pygame.K_RIGHT:
                    player.stop_right()
                elif event.key == pygame.K_UP:
                    player.stop_up()
                elif event.key == pygame.K_DOWN:
                    player.stop_down()

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 and not paused:
                is_shooting = True
                if bullet_counter > 0:
                    bullet = Peluru(player.rect.centerx, player.rect.top)
                    peluru.add(bullet)
                    bullet_counter -= 1
            elif event.button == 7:
                paused = not paused
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0 and player.original_image is not None:
                is_shooting = False

    if pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY and is_shooting and not paused:
        if bullet_counter > 0:
            last_shot_time = pygame.time.get_ticks()
            bullet = Peluru(player.rect.centerx, player.rect.top)
            peluru.add(bullet)
            bullet_counter -= 1

    if joystick:
        if not paused:
            move_player_with_joystick(joystick, player)

    if paused:
        font = pygame.font.SysFont('Comic Sans MS', 40)
        text = font.render("PAUSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()

    if not paused:
        move_player(keys, player)

        screen.blit(current_image, (0, bg_y_shift))
        background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
        background_top_rect.top = bg_y_shift + HEIGHT
        screen.blit(background_top, background_top_rect)

    bg_y_shift += 1
    if bg_y_shift >= 0:
        bg_y_shift = -HEIGHT

    if score > 3000:
        bg_y_shift += 2

    if score >= 3000 and not new_background_activated:
        current_image = background_img2
        background_top = background_img2.copy()
        new_background_activated = True

    if score >= 10000 and new_background_activated:
        current_image = background_img3
        background_top = background_img3.copy()

    if score >= 15000 and new_background_activated:
        current_image = background_img4
        background_top = background_img4.copy()

    if score == 0:
        current_image = background_img
        background_top = background_img.copy()
        new_background_activated = False

    screen.blit(current_image, (0, bg_y_shift))
    background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
    background_top_rect.top = bg_y_shift + HEIGHT
    screen.blit(background_top, background_top_rect)

    if score > hi_score:
        hi_score = score

    if random.randint(0, 120) == 0:
        enemy_img = random.choice(musuh1_img)
        musuh_object = Musuh1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            enemy_img,
        )
        musuh1_group.add(musuh_object)

    if score >= 3000 and random.randint(0, 40) == 0 and len(musuh2_group) < 2:
        enemy_img = random.choice(musuh2_img)
        musuh2_object = Musuh2(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            enemy_img,
        )
        musuh2_group.add(musuh2_object)

    if score >= 5000 and not dino1_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        dino1_img = dino1_img
        dino1_object = Dino1(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            dino1_img,
        )
        dino1_group.add(dino1_object)
        dino1_spawned = True

    if score >= 10000 and not dino2_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        dino2_img = dino2_img
        dino2_object = Dino2(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            dino2_img,
        )
        boss2_group.add(dino2_object)
        dino2_spawned = True

    if score >= 15000 and not dino3_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        dino3_img = dino3_img
        dino3_object = Dino3(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            dino3_img,
        )
        dino3_group.add(dino3_object)
        dino3_spawned = True

    if random.randint(0, 60) == 0:
        extra_score = ExtraScore(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50 - extra_score_img.get_rect().height),
            extra_score_img,
        )

        extra_score_group.add(extra_score)

    if score > 3000 and random.randint(0, 100) == 0:
        meteor_img = random.choice(peternak_imgs)
        orang_object = Peternak(
            random.randint(0, 50),
            random.randint(0, 50),
            meteor_img,
        )
        orang_group.add(orang_object)

    if random.randint(0, 90) == 0:
        meteor2_img = random.choice(peternak2_imgs)
        orang2_object = Peternak2(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - meteor2_img.get_rect().height),
            meteor2_img,
        )
        orang2_group.add(orang2_object)

    if player_life <= 0:
        show_game_over(score)
        dino1_spawned = False
        dino1_health = 150
        dino2_spawned = False
        dino2_health = 150
        dino3_spawned = False
        dino3_health = 200
        score = 0
        player_life = 200
        bullet_counter = 200
        player.rect.topleft = initial_player_pos
        peluru.empty()
        peluru_refill_group.empty()
        health_refill_group.empty()
        double_refill_group.empty()
        extra_score_group.empty()
        orang_group.empty()
        orang2_group.empty()
        musuh1_group.empty()
        musuh2_group.empty()
        dino1_group.empty()
        boss2_group.empty()
        dino3_group.empty()
        explosions.empty()
        explosions2.empty()


    for peluru_refill in peluru_refill_group:

        peluru_refill.update()
        peluru_refill.draw(screen)

        if player.rect.colliderect(peluru_refill.rect):
            if bullet_counter < 200:
                bullet_counter += 50
                if bullet_counter > 200:
                    bullet_counter = 200
                peluru_refill.kill()
                peluru_refill.sound_effect.play()
            else:
                peluru_refill.kill()
                peluru_refill.sound_effect.play()

    for health_refill in health_refill_group:
        health_refill.update()
        health_refill.draw(screen)

        if player.rect.colliderect(health_refill.rect):
            if player_life < 200:
                player_life += 50
                if player_life > 200:
                    player_life = 200
                health_refill.kill()
                health_refill.sound_effect.play()
            else:
                health_refill.kill()
                health_refill.sound_effect.play()

    for extra_score in extra_score_group:
        extra_score.update()
        extra_score.draw(screen)

        if player.rect.colliderect(extra_score.rect):
            score += 20
            extra_score.kill()
            extra_score.sound_effect.play()

        if score >= 3000:
            extra_score.speed = 2
        if score >= 10000:
            extra_score.speed = 4
        if score >= 15000:
            extra_score.speed = 6
        if score >= 20000:
            extra_score.speed = 8

    for double_refill in double_refill_group:
        double_refill.update()
        double_refill.draw(screen)

        if player.rect.colliderect(double_refill.rect):
            if player_life < 200:
                player_life += 50
                if player_life > 200:
                    player_life = 200
            if bullet_counter < 200:
                bullet_counter += 50
                if bullet_counter > 200:
                    bullet_counter = 200
                double_refill.kill()
                double_refill.sound_effect.play()
            else:
                double_refill.kill()
                double_refill.sound_effect.play()

    for orang_object in orang_group:
        orang_object.update()
        orang_object.draw(screen)

        if orang_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(orang_object.rect.center, explosion_images)
            explosions.add(explosion)
            orang_object.kill()
            score += 50

        peluru_collisions = pygame.sprite.spritecollide(orang_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion = Explosion(orang_object.rect.center, explosion_images)
            explosions.add(explosion)
            orang_object.kill()
            score += 80

            if random.randint(0, 10) == 0:
                double_refill = DoubleRefill(
                    orang_object.rect.centerx,
                    orang_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        if score >= 3000:
            orang_object.speed = 4
        if score >= 10000:
            orang_object.speed = 6
        if score >= 15000:
            orang_object.speed = 8
        if score >= 20000:
            orang_object.speed = 10

    for orang2_object in orang2_group:
        orang2_object.update()
        orang2_object.draw(screen)

        if orang2_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(orang2_object.rect.center, explosion_images)
            explosions.add(explosion)
            orang2_object.kill()
            score += 20

        peluru_collisions = pygame.sprite.spritecollide(orang2_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion = Explosion(orang2_object.rect.center, explosion_images)
            explosions.add(explosion)
            orang2_object.kill()
            score += 40

            if random.randint(0, 20) == 0:
                double_refill = DoubleRefill(
                    orang2_object.rect.centerx,
                    orang2_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        if score >= 3000:
            orang2_object.speed = 4
        if score >= 10000:
            orang2_object.speed = 6
        if score >= 15000:
            orang2_object.speed = 8
        if score >= 20000:
            orang2_object.speed = 10

    for musuh_object in musuh1_group:
        musuh_object.update(musuh1_group)
        musuh1_group.draw(screen)

        if musuh_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(musuh_object.rect.center, explosion_images)
            explosions.add(explosion)
            musuh_object.kill()
            score += 20

        peluru_collisions = pygame.sprite.spritecollide(musuh_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion = Explosion(musuh_object.rect.center, explosion_images)
            explosions.add(explosion)
            musuh_object.kill()
            score += 50

            if random.randint(0, 8) == 0:
                peluru_refill = BulletRefill(
                    musuh_object.rect.centerx,
                    musuh_object.rect.centery,
                    peluru_refill_img,
                )
                peluru_refill_group.add(peluru_refill)

            if random.randint(0, 8) == 0:
                health_refill = HealthRefill(
                    random.randint(50, WIDTH - 30),
                    random.randint(-HEIGHT, -30),
                    health_refill_img,
                )
                health_refill_group.add(health_refill)

    for musuh2_object in musuh2_group:
        musuh2_object.update(musuh2_group, musuh2_peluru, player)
        musuh2_group.draw(screen)
        musuh2_peluru.update()
        musuh2_peluru.draw(screen)

        if musuh2_object.rect.colliderect(player.rect):
            player_life -= 40
            explosion2 = Explosion2(musuh2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            musuh2_object.kill()
            score += 20

        peluru_collisions = pygame.sprite.spritecollide(musuh2_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion2 = Explosion2(musuh2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            musuh2_object.kill()
            score += 80

            if random.randint(0, 20) == 0:
                double_refill = DoubleRefill(
                    musuh2_object.rect.centerx,
                    musuh2_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        for musuh2_bullet in musuh2_peluru:
            if musuh2_bullet.rect.colliderect(player.rect):
                player_life -= 10
                explosion = Explosion(player.rect.center, explosion3_images)
                explosions.add(explosion)
                musuh2_bullet.kill()

    for dino1_object in dino1_group:
        dino1_object.update(dino1_peluru, player)
        dino1_group.draw(screen)
        dino1_peluru.update()
        dino1_peluru.draw(screen)

        if dino1_object.rect.colliderect(player.rect):
            player_life -= 20
            explosion = Explosion2(dino1_object.rect.center, explosion2_images)
            explosions2.add(explosion)

        peluru_collisions = pygame.sprite.spritecollide(dino1_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion2 = Explosion(dino1_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            dino1_health -= 5
            if dino1_health <= 0:
                explosion = Explosion2(dino1_object.rect.center, explosion3_images)
                explosions.add(explosion)
                dino1_object.kill()
                score += 400

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        dino1_object.rect.centerx,
                        dino1_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        for dino1_bullet in dino1_peluru:
            if dino1_bullet.rect.colliderect(player.rect):
                player_life -= 20
                explosion = Explosion(player.rect.center, explosion3_images)
                explosions.add(explosion)
                dino1_bullet.kill()

        if dino1_health <= 0:
            explosion = Explosion2(dino1_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            dino1_object.kill()

    if dino1_group:
        dino1_object = dino1_group.sprites()[0]
        dino1_health_bar_rect.center = (dino1_object.rect.centerx, dino1_object.rect.top - 5)
        pygame.draw.rect(screen, (255, 0, 0), dino1_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (dino1_health_bar_rect.left, dino1_health_bar_rect.top, dino1_health, dino1_health_bar_rect.height))

    for dino2_object in boss2_group:
        dino2_object.update(dino2_peluru, player)
        boss2_group.draw(screen)
        dino2_peluru.update()
        dino2_peluru.draw(screen)

        if dino2_object.rect.colliderect(player.rect):
            player_life -= 2
            explosion2 = Explosion2(dino2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)

        peluru_collisions = pygame.sprite.spritecollide(dino2_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion2 = Explosion2(dino2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            dino2_health -= 8
            if dino2_health <= 0:
                explosion2 = Explosion2(dino2_object.rect.center, explosion3_images)
                explosions2.add(explosion2)
                dino2_object.kill()
                score += 800

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        dino2_object.rect.centerx,
                        dino2_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        for dino2_bullet in dino2_peluru:
            if dino2_bullet.rect.colliderect(player.rect):
                player_life -= 20
                explosion = Explosion(player.rect.center, explosion3_images)
                explosions.add(explosion)
                dino2_bullet.kill()

        if dino2_health <= 0:
            explosion = Explosion2(dino2_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            dino2_object.kill()

    if boss2_group:
        dino2_object = boss2_group.sprites()[0]
        dino2_health_bar_rect.center = (dino2_object.rect.centerx, dino2_object.rect.top - 5)
        pygame.draw.rect(screen, (255, 0, 0), dino2_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (dino2_health_bar_rect.left, dino2_health_bar_rect.top, dino2_health, dino2_health_bar_rect.height))

    for dino3_object in dino3_group:
        dino3_object.update(dino3_peluru, player)
        dino3_group.draw(screen)
        dino3_peluru.update()
        dino3_peluru.draw(screen)

        if dino3_object.rect.colliderect(player.rect):
            player_life -= 1
            explosion2 = Explosion2(dino3_object.rect.center, explosion2_images)
            explosions2.add(explosion2)

        peluru_collisions = pygame.sprite.spritecollide(dino3_object, peluru, True)
        for peluru_collision in peluru_collisions:
            explosion2 = Explosion2(dino3_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            dino3_health -= 6
            if dino3_health <= 0:
                explosion2 = Explosion2(dino3_object.rect.center, explosion3_images)
                explosions2.add(explosion2)
                dino3_object.kill()
                score += 1000

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        dino3_object.rect.centerx,
                        dino3_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        for dino3_bullet in dino3_peluru:
            if dino3_bullet.rect.colliderect(player.rect):
                player_life -= 20
                explosion = Explosion(player.rect.center, explosion3_images)
                explosions.add(explosion)
                dino3_bullet.kill()

        if dino3_health <= 0:
            explosion = Explosion2(dino3_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            dino3_object.kill()

    if dino3_group:
        dino3_object = dino3_group.sprites()[0]
        dino3_health_bar_rect.center = (dino3_object.rect.centerx, dino3_object.rect.top - 5)
        pygame.draw.rect(screen, (255, 0, 0), dino3_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (dino3_health_bar_rect.left, dino3_health_bar_rect.top, dino3_health, dino3_health_bar_rect.height))

    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    for explosion2 in explosions2:
        explosion2.update()
        screen.blit(explosion2.image, explosion2.rect)

    for bullet in peluru:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)

        if bullet.rect.bottom < 0:
            bullet.kill()
            bullet_counter -= 1

    player_life_surface = pygame.Surface((200, 25), pygame.SRCALPHA, 32)
    player_life_surface.set_alpha(216)

    player_life_bar_width = int(player_life / 200 * 200)
    player_life_bar_width = max(0, min(player_life_bar_width, 200))

    player_life_bar = pygame.Surface((player_life_bar_width, 30), pygame.SRCALPHA, 32)
    player_life_bar.set_alpha(216)

    life_bar_image = pygame.image.load("images/life_bar.png").convert_alpha()

    if player_life > 50:
        player_life_bar.fill((152, 251, 152))
    else:
        player_life_bar.fill((0, 0, 0))

    player_life_surface.blit(life_bar_image, (0, 0))
    player_life_surface.blit(player_life_bar, (35, 0))

    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    peluru_counter_surface = pygame.Surface((200, 25), pygame.SRCALPHA, 32)
    peluru_counter_surface.set_alpha(216)
    peluru_counter_bar = pygame.Surface(((bullet_counter / 200) * 200, 30), pygame.SRCALPHA, 32)
    peluru_counter_bar.set_alpha(216)
    bullet_bar_image = pygame.image.load("images/bullet_bar.png").convert_alpha()
    if bullet_counter > 50:
        peluru_counter_bar.fill((255, 23, 23))
    else:
        peluru_counter_bar.fill((0, 0, 0))
    peluru_counter_surface.blit(bullet_bar_image, (0, 0))
    peluru_counter_surface.blit(peluru_counter_bar, (35, 0))
    peluru_x_pos = 10
    peluru_y_pos = player_life_surface.get_height() + 20
    screen.blit(peluru_counter_surface, (peluru_x_pos, peluru_y_pos))

    score_surface = pygame.font.SysFont('Comic Sans MS', 30).render(f'{score}', True, (238, 232, 170))
    score_image_rect = score_surface.get_rect()
    score_image_rect.x, score_image_rect.y = WIDTH - score_image_rect.width - extra_score_img.get_width() - 10, 10

    screen.blit(extra_score_img, (score_image_rect.right + 5, score_image_rect.centery - extra_score_img.get_height()//2))
    screen.blit(score_surface, score_image_rect)

    hi_score_surface = pygame.font.SysFont('Comic Sans MS', 20).render(f'HI-SCORE: {hi_score}', True, (255, 255, 255))
    hi_score_surface.set_alpha(128)
    hi_score_x_pos = (screen.get_width() - hi_score_surface.get_width()) // 2
    hi_score_y_pos = 0
    screen.blit(hi_score_surface, (hi_score_x_pos, hi_score_y_pos))

    pygame.display.flip()

    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
