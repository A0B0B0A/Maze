from pygame import *
import random

init()
mixer.init()
mixer.music.load('Cypis_-_Polskaya_Korova.mp3')
mixer.music.play()
mixer.music.set_volume(0.3)

font.init()

font1 = font.SysFont('Impact', 100)
game_over_text = font1.render("Game Over!", True, (255, 0, 0))

MAP_WIDTH, MAP_HEIGHT = 25, 20
TILESIZE = 30

WIDTH, HEIGHT = MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE
window = display.set_mode((WIDTH, HEIGHT))
FPS = 90
clock = time.Clock()

bg = image.load('background.jpg')
bg = transform.scale(bg,(WIDTH, HEIGHT))

p_img = image.load('hero.png')
warrior_img = image.load('korova.png')
wall_img = image.load('wall.png')
treasure_img = image.load('treasure.png')

all_sprites = sprite.Group()

class NPC(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(NPC):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 1

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
        
        bos_hit = sprite.spritecollide(self, boses, False, sprite.collide_mask)
        if len(bos_hit):
            self.hp -= 100

     
class Bos(NPC):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 100
        self.speed = 1
        self.dir_list = ['right', 'left', 'up', 'down']
        self.dir = random.choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed
        
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)
            

player = Player(p_img, 20, 20, 300, 300)
walls = sprite.Group()
boses = sprite.Group()
with open("map.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w":#стіни
                walls.add(NPC(wall_img, TILESIZE, TILESIZE, x, y ))
            if symbol == "p":#гравець
                player.rect.x = x
                player.rect.y = y
            if symbol == "t":
                treasure = NPC(treasure_img, TILESIZE, TILESIZE, x, y)
            if symbol == "b":
                boses.add(Bos(warrior_img, TILESIZE, TILESIZE, x, y))
            x += TILESIZE
        y += TILESIZE
        x = 0

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.blit(bg,(0,0))
    
    if player.hp <= 0 :
        finish = True
    
    if sprite.collide_mask(player, treasure):
        finich = True
        game_over_text = font1.render("You win!", True, (0, 255, 0))
        
    all_sprites.draw(window)

    if not finish:
        all_sprites.update()
  
    if finish:
        window.blit(game_over_text, (170, 230))

    display.update()
    clock.tick(FPS)