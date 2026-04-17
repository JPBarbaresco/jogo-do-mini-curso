import pygame
import random
import sys
from pygame.locals import K_a, K_d, K_SPACE

SCREEN_SIZE = SCREEN_X, SCREEN_Y = 600, 800

FPS = 60

PLAYER_SPEED = 10

BULLET_SPEED = 15

POWER_UPS = ["imunity", "fire rate", "extra live", "ultra shot"]

pygame.init()

class Player(pygame.sprite.Sprite): #AKA Shrek low poly
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.Surface((60, 60))
        self.rect = self.surf.get_rect(center = (SCREEN_X//2, SCREEN_Y-100))

        self.surf.set_colorkey((0,0,0))

        pygame.draw.polygon(self.surf, (0, 255, 0), [(0,60), (30,0), (60,60)])

        self.mask = pygame.mask.from_surface(self.surf)
    
    def update(self, pressed_keys):
        if pressed_keys[K_a]:
            self.rect.move_ip((-PLAYER_SPEED, 0))
        elif pressed_keys[K_d]:
            self.rect.move_ip((PLAYER_SPEED, 0))

        if self.rect.right > SCREEN_X:
            self.rect.right = SCREEN_X
        elif self.rect.left < 0:
            self.rect.left = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Bullet, self).__init__()

        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect(center = position)

        self.surf.set_colorkey((0,0,0))

        pygame.draw.circle(self.surf, (255, 255, 255), (10,10), 10)
    
    def update(self):
        self.rect.move_ip((0, -BULLET_SPEED))

        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Enemy, self).__init__()

        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect(center = position)

        self.surf.set_colorkey((0,0,0))

        pygame.draw.polygon(self.surf, (255,0,0), ((0,0), (30,0), (15,30)))

        self.mask = pygame.mask.from_surface(self.surf)

    def update(self):
        self.rect.move_ip((0, 5))

        if self.rect.top > SCREEN_Y:
            if random.choice([True, False]):
                self.rect.top = random.randint(-3000, -200)
            else:
                self.kill()

class Buttom(pygame.Surface):
    def __init__(self, size, color, text, text_color, font : pygame.font.Font, position):
        super().__init__(size)

        self.rect = self.get_rect(center = position)
        self.color = color

        self.got_pressed = False

        self.set_colorkey((0,0,0))

        pygame.draw.rect(self, color, self.get_rect(), border_radius= 20)
        self.text = font.render(text, False, text_color)
        self.blit(self.text, self.text.get_rect(center = self.get_rect().center))
    
    def update(self, pointer = None) -> bool:
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if pointer is None:
            pointer = pygame.mouse.get_pos()
        self.fill((0,0,0))
        if self.rect.collidepoint(pointer) and mouse_pressed:
            color = []
            for color_value in self.color:
                if color_value > 50:
                    color += [color_value-50]
                else:
                    color += [0]
                
            pygame.draw.rect(self, color, self.get_rect(), border_radius= 20)
            self.blit(self.text, self.text.get_rect(center = self.get_rect().center))
            self.got_pressed = True
            return False
        
        elif self.got_pressed and self.rect.collidepoint(pointer):
            pygame.draw.rect(self, self.color, self.get_rect(), border_radius= 20)
            self.blit(self.text, self.text.get_rect(center = self.get_rect().center))
            self.got_pressed = False
            return True
        
        else:
            pygame.draw.rect(self, self.color, self.get_rect(), border_radius= 20)
            self.blit(self.text, self.text.get_rect(center = self.get_rect().center))
            return False

class PowerUP(pygame.sprite.Sprite):
    def __init__(self, type, life_time, position, frames):
        super(PowerUP, self).__init__()

        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect(center = position)

        self.frames_0 = frames
        self.life_time = life_time
        self.type = type
        self.colors = [(0,0,255), (255,255,255)]
        self.color = 0

    def update(self, frames):
        self.rect.move_ip((0, 2))

        if frames %5 == 0:
            self.color = (self.color+1)%len(self.colors)

        self.surf.fill(self.colors[self.color])

        if self.rect.top > SCREEN_Y:
            self.kill()
    

def play():
    global frames_since_enemy
    global frames_since_shooted
    
    global game_over
    
    global score
    global lives
    global frames
    global score_treshold

    global invincible
    global invincibility_cool_down

    pressed_keys = pygame.key.get_pressed()

    if frames_since_enemy >= 15:
        enemy = Enemy((random.randint(20, SCREEN_X-20), random.randint(-50, -20)))
        all_enemys.add(enemy)
        all_sprites.add(enemy)

        frames_since_enemy = 0
    else:
        frames_since_enemy += 1

    if pressed_keys[K_SPACE] and frames_since_shooted >= 10:
        bullet = Bullet(player.rect.center)
        all_bullets.add(bullet)
        all_sprites.add(bullet)
        frames_since_shooted = 0
    else:
        frames_since_shooted += 1

    if score > score_treshold and random.randint(0, 600) == 0:
        power_up = PowerUP(random.choice(POWER_UPS), 300, (random.randint(30, SCREEN_X-30),random.randint(-50, -10)), frames)
        all_POWER_UPS.add(power_up)

    player.update(pressed_keys)
    all_sprites.update()
    all_POWER_UPS.update(frames)

    for enemy in pygame.sprite.spritecollide(player, all_enemys, False):
        if pygame.sprite.collide_mask(player, enemy):
            if not invincible:
                lives -= 1
            game_surface.fill((255,0,0))
            enemy.kill()
        
    if lives <= 0:
        game_over = True
    
    colisions = pygame.sprite.groupcollide(all_bullets, all_enemys, True, True)
    if len(colisions) > 0:
        score += len(colisions)

    for power_up in pygame.sprite.spritecollide(player, all_POWER_UPS, False):
        if power_up.type == 'imunity':
            invincible = True
            invincibility_cool_down = power_up.life_time
            power_up.kill()
            score_treshold += score + 30
            print('collected power up')
    
    if invincible:
        invincibility_cool_down -= 1
        if invincibility_cool_down <= 0:
            invincible = False

    score_text = score_font.render(f"score: {score}", False, (255,255,255))
    lives_text = score_font.render(f"vidas: {lives}", False, (255,255,255))

    draw_objects()

    game_surface.blit(score_text, (10,SCREEN_Y-40))
    game_surface.blit(lives_text, (SCREEN_X//2,SCREEN_Y-40))

def game_over_screen():
    global game_over
    global lives
    global score_treshold
    global frames_since_enemy
    global frames_since_shooted

    text = game_over_font.render("GAME OVER", False, (255,0,0))
    text_rect = text.get_rect(center = (SCREEN_X//2, SCREEN_Y//2))

    stats = score_font.render(f'score: {score}', False, (255,0,0))
    stats_rect = stats.get_rect(center = (SCREEN_X//2, SCREEN_Y//2 + (text_rect.bottom - text_rect.top)))

    draw_objects()
    
    pygame.draw.rect(game_surface, (0,0,0), (0, text_rect.y-15, SCREEN_X, (text_rect.bottom - text_rect.top)+20))
    
    if full_screen:
        scaled_surface_size = ((screen.get_height()*SCREEN_X//SCREEN_Y), screen.get_height())
        scaled_surface_rect = pygame.Rect((screen.get_width() - scaled_surface_size[0]) // 2, (screen.get_height() - scaled_surface_size[1]) // 2, scaled_surface_size[0], scaled_surface_size[1])
        scale_x = scaled_surface_size[0] / SCREEN_X
        scale_y = scaled_surface_size[1] / SCREEN_Y
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse = ((mouse_pos[0] - scaled_surface_rect.left) / scale_x, (mouse_pos[1] - scaled_surface_rect.top) / scale_y)
        reset = reset_buttom.update(adjusted_mouse)
    else:
        reset = reset_buttom.update()
    
    if reset:
        game_over = False
        score = 0
        lives = 5
        score_treshold = 30
        for power_up in all_POWER_UPS:
            power_up.kill()
        for sprite in all_sprites:
            sprite.kill()
        frames_since_shooted = 0
        frames_since_enemy = 0
        player.rect.center = (SCREEN_X//2, SCREEN_Y-100)
    
    game_surface.blit(text, text_rect)
    game_surface.blit(stats, stats_rect)
    game_surface.blit(reset_buttom, reset_buttom.rect)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Aula 1 - Movimento do Jogador")

score_font = pygame.font.SysFont('pressstart2pregular', 20)
game_over_font = pygame.font.SysFont('pressstart2pregular', 60)

clock = pygame.time.Clock()

game_surface = pygame.Surface(SCREEN_SIZE)

def draw_objects(surface=game_surface):
    global player
    global all_sprites
    global invincible

    surface.blit(player.surf, player.rect)

    if invincible:
        pygame.draw.circle(surface, (0,0,255), player.rect.center, 60, 5)

    for power_up in all_POWER_UPS:
        surface.blit(power_up.surf, power_up.rect)
    
    for sprite in all_sprites:
        surface.blit(sprite.surf, sprite.rect)

player = Player()

reset_buttom = Buttom((2*SCREEN_X//3, SCREEN_Y//16), (255,0,0), 'Tentar Novamente?', (1,1,1), score_font, (SCREEN_X//2, 3*SCREEN_Y//4))

all_bullets = pygame.sprite.Group()
all_enemys = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_POWER_UPS = pygame.sprite.Group()

frames_since_shooted = 0
frames_since_enemy = 0

score = 0
game_over = False
lives = 5
score_treshold = 30

invincible = False
invincibility_cool_down = 0
fire_rate_power_up = False
fire_rate_power_up_cool_down = 0

running = True
full_screen = False
frames = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            full_screen = not full_screen
            if full_screen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(SCREEN_SIZE)

    if game_over:
        game_surface.fill((0, 0, 75))
        game_over_screen()   
    else:
        game_surface.fill((0, 75, 150))
        play()

    if full_screen:
        scaled_surface_size = ((screen.get_height()*SCREEN_X//SCREEN_Y), (screen.get_height()))
        scaled_surface = pygame.transform.scale(game_surface, scaled_surface_size)
        scaled_surface_rect = scaled_surface.get_rect(center = (screen.get_width()//2, screen.get_height()//2))
        screen.blit(scaled_surface, scaled_surface_rect)
    else:
        screen.blit(game_surface, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

    frames += 1