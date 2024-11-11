import pygame
import random
import time

from Bullet import Bullet
from Enemy import Enemy
from Player import Player
from Sounds import Sounds

def init_enemies(images):
    enemies = []
    for i in range(0, 11, 1):
        enemies.append(Enemy(images[4], images[5], (i * 62.5) + 100, 150, 2, 30))
    for i in range(0, 11, 1):
        enemies.append(Enemy(images[0], images[1], (i * 62.5) + 100, 200, 0, 20))
    for i in range(0, 11, 1):
        enemies.append(Enemy(images[0], images[1], (i * 62.5) + 100, 250, 0, 20))
    for i in range(0, 11, 1):
        enemies.append(Enemy(images[2], images[3], (i * 62.5) + 100, 300, 1, 10))
    for i in range(0, 11, 1):
        enemies.append(Enemy(images[2], images[3], (i * 62.5) + 100, 350, 1, 10))
    return enemies

def increase_enemy_speed(enemies, speed):
    for i in range(len(enemies)):
        enemies[i].anim_speed += 0.001
        if(enemies[i].vel_x < 0):
            enemies[i].vel_x -= speed   
        else:
            enemies[i].vel_x += speed   

def shift_enemies_down(enemies, offset):
    for i in range(len(enemies)):
        if(enemies[i].type != 3):
            enemies[i].vel_x *= -1
            enemies[i].x += offset
            enemies[i].y += 25

def enemy_shoot(enemies, enemy_bullets):
    enemy = random.choice(enemies)
    enemy_bullet = Bullet((enemy.x + enemy.width // 2) - 4, enemy.y, 4, 16)
    enemy_bullet.vel_y = 6
    enemy_bullets.append(enemy_bullet)

def spawn_ufo(image, ufo, width):
    start = random.choice([(-32, 2), (width+32, -2)])
    points = [50, 100, 150, 200, 250, 300]
    ship = Enemy(image, image, start[0], 100, 3, random.choice(points))
    ship.vel_x = start[1]
    ufo.append(ship)

def read_high_score(filename):
    f = open(filename, "r")
    high_score = int(f.read())
    f.close()
    return high_score

def write_high_score(filename, score):
    f = open(filename, "w")
    f.write("{}".format(score))
    f.close()
    return True

def update(player, player_bullets, enemies, enemy_bullets, sounds, ufo, width):
    player.update()

    for i in range(len(player_bullets)):
        player_bullets[i].update()

    for i in range(len(enemies)):
        enemies[i].update()
    
    for i in range(len(enemy_bullets)):
        enemy_bullets[i].update()

    for i in range(len(ufo)):
        ufo[i].update()
    
    for i in range(len(enemies)):
        if enemies[i].x <= 0:
            shift_enemies_down(enemies, 1)
            break
        if(enemies[i].x >= width - 32):
            shift_enemies_down(enemies, -1)
            break

    for u in ufo:
        if u.x < -32 or u.x > width + 32:
            ufo.remove(u)
            if sounds.ufo_sound_playing():
                sounds.ufo_entered.stop()

    for bullet in player_bullets:
        for enemy in enemies:
            if pygame.Rect.colliderect(pygame.Rect(bullet.collision_rect()), pygame.Rect(enemy.collision_rect())):
                player.score += enemy.points
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                sounds.enemy_killed.play()
                increase_enemy_speed(enemies, random.uniform(0, 0.1))
        for u in ufo:
            if pygame.Rect.colliderect(pygame.Rect(bullet.collision_rect()), pygame.Rect(u.collision_rect())):
                player.score += u.points
                player_bullets.remove(bullet)
                ufo.remove(u)
                if sounds.ufo_sound_playing():
                    sounds.ufo_entered.stop()
                sounds.ufo_dieing.play()
                
    for bullet in enemy_bullets:
        if pygame.Rect.colliderect(pygame.Rect(bullet.collision_rect()), pygame.Rect(player.collision_rect())):
            enemy_bullets.remove(bullet)
            player.lives -= 1
            sounds.player_dieing.play()
            #respawn player
            print("Player hit")
    for enemy in enemies:
        if pygame.Rect.colliderect(pygame.Rect(enemy.collision_rect()), player.collision_rect()): 
            player.lives -= 1
            print("Game over")
            pass
    

def draw(screen, background, font, player, player_bullets, enemies, enemy_bullets, ufo, width, height, high_score):
    screen.blit(background, (0, 0))

    player_1_score_title = font.render("SCORE < 1 >", False, (255, 255, 255))
    screen.blit(player_1_score_title, (50, 0))
    player_1_score = font.render("{}".format(player.score), False, (255, 255, 255))
    screen.blit(player_1_score, (100, 60))
    high_score_title = font.render("HI-SCORE", False, (255, 255, 255))
    screen.blit(high_score_title, ((width//2)-100, 0))
    high_score_text = font.render("{}".format(high_score), False, (255, 255, 255))
    screen.blit(high_score_text, ((width//2)-50, 60))
    player_2_score_title = font.render("SCORE < 2 >", False, (255, 255, 255))
    screen.blit(player_2_score_title, (width-250, 0))
    pygame.draw.line(screen, (0, 255, 0), (0, height-50),(width, height-50), 4)
    player_lives = font.render("{}".format(player.lives), False, (255, 255, 255))
    screen.blit(player_lives, (10, height - 48))
    credit = font.render("CREDIT   0 0", False, (255, 255, 255))
    screen.blit(credit, (width - 250, height - 35))

    player.draw(screen)
    for i in range(len(player_bullets)):
        player_bullets[i].draw(screen)
    for i in range(len(enemies)):
        enemies[i].draw(screen)
    for i in range(len(enemy_bullets)):
        enemy_bullets[i].draw(screen)
    for i in range(len(ufo)):
        ufo[i].draw(screen)

    pygame.display.flip()

def main():
    pygame.init()
    font = pygame.font.Font('Space Invaders Python/Resources/fonts/space_invaders.ttf', 28)
    player_ship = pygame.image.load('Space Invaders Python/Resources/images/player ship.png')
    enemy_1_image_1 = pygame.image.load('Space Invaders Python/Resources/images/Crab (1).png')
    enemy_1_image_2 = pygame.image.load('Space Invaders Python/Resources/images/Crab (2).png')
    enemy_2_image_1 = pygame.image.load('Space Invaders Python/Resources/images/Octopus (1).png')
    enemy_2_image_2 = pygame.image.load('Space Invaders Python/Resources/images/Octopus (2).png')
    enemy_3_image_1 = pygame.image.load('Space Invaders Python/Resources/images/Squid (1).png')
    enemy_3_image_2 = pygame.image.load('Space Invaders Python/Resources/images/Squid (2).png')
    enemy_4_image = pygame.image.load('Space Invaders Python/Resources/images/UFO.png')
    enemy_images = [enemy_1_image_1, enemy_1_image_2, enemy_2_image_1, enemy_2_image_2, enemy_3_image_1, enemy_3_image_2]
    #pygame.mixer.music.load('Space Invaders Python/Resources/sounds/05-Attack of the Invaders.wav')
    width = height = 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Space Invaders')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    high_score = read_high_score("Space Invaders Python/high score.txt")
    sounds = Sounds()
    player_bullets = []
    enemies = []
    ufo = []
    enemy_bullets = []
    enemies = init_enemies(enemy_images)
    player = Player(player_ship, width // 2, height - 100)
    level = 1
    running = True
    FPS = 60
    clock = pygame.time.Clock()
    enemy_shooting_timer = time.time()

    while(running):
        clock.tick(FPS)
        # game over
        if player.lives == 0:
            if(high_score < player.score):
                write_high_score("Space Invaders Python\high score.txt", player.score)
            running = False
        # reset
        if len(enemies) == 0:
            level += 1
            enemies = init_enemies(enemy_images)
            player_bullets = []
            enemy_bullets = []
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
        key = pygame.key.get_pressed()
        if key[pygame.K_a] == True:
            player.vel_x = -2
        elif key[pygame.K_d] == True:
            player.vel_x = 2
        else:
            player.vel_x = 0

        if key[pygame.K_SPACE] == True and len(player_bullets) < 1:
            player_bullets.append(Bullet((player.x + player.width // 2) - 4, player.y, 3, 8))  
            sounds.player_shooting.play()
        
        player_bullets = [b for b in player_bullets if b.y > 100]
        if(time.time() - enemy_shooting_timer >= 2):
            enemy_shoot(enemies, enemy_bullets)
            enemy_shooting_timer = time.time()
        if len(ufo) == 0 and random.randrange(0, 7500) == 1:
            spawn_ufo(enemy_4_image, ufo, width)
            sounds.play_ufo_sound()
        
        update(player, player_bullets, enemies, enemy_bullets, sounds, ufo, width)
        draw(screen, background, font, player, player_bullets, enemies, enemy_bullets, ufo, width, height, high_score)
        
if __name__ == '__main__': main()