from pygame import *
from random import randint
from time import time as timer
mixer.init()

win_w = 700
win_h = 700 

main_win = display.set_mode((win_w,win_h))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700,700))

#Музыка
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.music.load('fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, size_x, size_y, player_speed, player_x, player_y, s2):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.s2 = s2
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.image_name = player_image
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()     
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 625:
            self.rect.x += self.speed  
    def fire(self):
        bullet1 = Bullet("bullet.png", 15, 20, -7, self.rect.centerx, self.rect.top, randint(-3, 3))
        bullets.add(bullet1)
        if number_def_enemy >= 15:
            bullet2 = Bullet("bullet.png", 15, 20, -35, self.rect.centerx, self.rect.top, 0)
            super_bullets.add(bullet2)
            bullets.remove(bullet1)



class Enemy(GameSprite):
    def update(self):
        global number_lost_enemy
        self.rect.y += self.speed
        self.rect.x += self.s2
        if self.rect.y >= 700:
            self.rect.x = randint(0, 625)
            if self.image_name != 'asteroid.png':
                self.rect.y = -60
                self.speed = randint(1, 2)                
                number_lost_enemy += 1
            else:
                self.rect.y = randint(-2000, -600)
    def mfire(self):
        # if number_def_enemy >= 20:
        if self.image_name != 'asteroid.png':
            now_time_mfire = timer()
            last_time_mfire = timer()
            if now_time_mfire - last_time_mfire < randint(3, 6):
                print('1')
                bullet = Bullet("bullet.png", 15, 20, 4, self.rect.centerx, self.rect.bottom, 0)
                monster_bullets.add(bullet)
                

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.s2
        if self.rect.y < 0:
            self.kill()


monster_bullets = sprite.Group()
super_bullets = sprite.Group()
bullets = sprite.Group()
player = Player('rocket.png', 65, 65, 8, 317.5, 630, 0)

p = 0
monsters = sprite.Group()
for i in range(1, 7):
    monsters.add(Enemy('ufo.png', 65, 65, randint(1, 2), randint(0, 625), -60, 0))
    p += 1


d = 0
asteroids = sprite.Group()
for i in range(1, 4):
    asteroids.add(Enemy('asteroid.png', 100, 100, 1, randint(0, 600), randint(-2000, -600), 0))
    d += 1



game = True
finish = False

font.init()
font = font.Font(None, 40)
win = font.render('YOU WIN!', True, (0, 255, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 0))


number_def_enemy = 0
number_lost_enemy = 0
number_fire = 0
reload_time = False


clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
            
                if number_fire < 5 and reload_time == False:
                    # fire_sound.play()
                    player.fire()
                    number_fire += 1   

                if number_fire >= 5 and reload_time == False:
                    last_time = timer()  
                    reload_time = True 

            # if number_def_enemy >= 20:
            #     now_time_fire = timer()
            #     self.Enemy
            #     if now_time_fire -last_time randint(3, 6):

        


    if finish != True:
        defeat_enemy = font.render('Врагов убито:' + str(number_def_enemy), 1, (255, 255, 255))
        lost_enemy = font.render('Врагов пропущено:' + str(number_lost_enemy), 1, (255, 255, 255))

        if sprite.groupcollide(monsters, bullets, True, True) or sprite.groupcollide(monsters, super_bullets, True, True):
            number_def_enemy += 1
            monsters.add(Enemy('ufo.png', 65, 65, randint(1, 2), randint(0, 625), 0, 0))

        sprite.groupcollide(asteroids, bullets, False, True)
        sprite.groupcollide(asteroids, super_bullets, False, False)
        sprite.groupcollide(monster_bullets, super_bullets, True, True)


        main_win.blit(background, (0, 0))   
        main_win.blit(defeat_enemy, (0, 0))  
        main_win.blit(lost_enemy, (0, 30)) 
        

        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        super_bullets.update()
        monster_bullets.update()

        player.reset()
        monsters.draw(main_win)
        asteroids.draw(main_win)
        bullets.draw(main_win)
        super_bullets.draw(main_win)
        monster_bullets.draw(main_win)



        if reload_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font.render('Wait, reload...', 1, (255, 0, 0))
                main_win.blit(reload, (260, 660))
            else:
                number_fire = 0
                reload_time = False
        
        if number_def_enemy == 100:
            finish = True
            main_win.blit(win, (300, 350))

        if sprite.spritecollide(player, monsters, False) or number_lost_enemy >= 3:
            finish = True
            main_win.blit(lose, (260, 350))

        if sprite.spritecollide(player, asteroids, False):
            finish = True
            main_win.blit(lose, (260, 350))


    display.update()      
    clock.tick(FPS)              