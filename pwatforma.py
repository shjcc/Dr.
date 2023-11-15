import pygame, math, os
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (90,500))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            
    def animation_state(self):
        if self.rect.bottom < 500:
            self.image = self.player_jump
        else:
            self.player_index += 0.12
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'flying':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 370
        else:
            ground_1 = pygame.image.load('graphics/ground/ground1.png').convert_alpha()
            ground_2 = pygame.image.load('graphics/ground/ground2.png').convert_alpha()
            self.frames = [ground_1,ground_2]    
            y_pos = 500

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1100,1400), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if score <= 20:
            self.rect.x -= 8

        elif score >= 20:  
            x = 0 + (score * 0.3)
            self.rect.x -= x
        # elif score >= 10 and score <= 20:
        #     self.rect.x -= 8

        # elif score >= 20 and score <= 30:
        #     self.rect.x -= 10

        # elif score >= 30 and score <= 40:
        #     self.rect.x -= 12   

        # elif score >= 40 and score <= 50:
        #     self.rect.x -= 14

        # elif score >= 50 and score <= 60:
        #     self.rect.x -= 16     

        # elif score >= 60 and score <= 70:
        #     self.rect.x -= 18

        # elif score >= 70 and score <= 80:
        #     self.rect.x -= 20 

        # elif score >= 80 and score <= 90:
        #     self.rect.x -= 22    

        # elif score >= 90 and score <= 100:
        #     self.rect.x -= 24

        # else:
        #     self.rect.x -= 30                                  

        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', True,  (25,175,150))
    score_rect = score_surf.get_rect(center = (500,148))
    screen.blit(score_surf, score_rect)
    return current_time

def display_score_bg():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', True,  (0,0,0))
    score_rect = score_surf.get_rect(center = (497,146))
    screen.blit(score_surf, score_rect)
    return current_time  

def display_message():
    hi1 = game_font.render('My patients NEED me!',False,(10, 10, 10))
    hi1_rect = hi1.get_rect(center = (150,300))
    if score > 0 and score < 10:
        screen.blit(hi1,hi1_rect)
    hi2 = game_font.render('Only ME, DR.Fart can save them!',False,(10, 10, 10))
    hi2_rect = hi2.get_rect(center = (250,300))
    if score > 20 and score < 30:
        screen.blit(hi2,hi2_rect)
    hi3 = game_font.render('Is that a flying cat...',False,(10, 10, 10))
    hi3_rect = hi3.get_rect(center = (250,300))
    if score > 40 and score < 50:
        screen.blit(hi3,hi3_rect) 
    hi4 = game_font.render('I literally have a car...',False,(10, 10, 10))
    hi4_rect = hi4.get_rect(center = (250,300))
    if score > 60 and score < 70:
        screen.blit(hi4,hi4_rect)        
    return hi1,hi2,hi3,hi4


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

# Initialise  
pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dr.Fart')
clock = pygame.time.Clock()
test_font = pygame.font.Font(os.path.abspath('font/Pixeltype.ttf'), 70)
game_font = pygame.font.Font(os.path.abspath('font/Pixeltype.ttf'), 40)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.play(loops = -1)

#GROUPS 
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()
clouds_surface = pygame.image.load('graphics/clouds.png').convert_alpha()
clouds_x_pos = 900
clouds_x1_pos = 300
buildings_1 = pygame.image.load('graphics/buildings_1.png').convert_alpha()
buildings_2 = pygame.image.load('graphics/buildings_2.png').convert_alpha()
buildings_3 = pygame.image.load('graphics/buildings_3.png').convert_alpha()
lamp = pygame.image.load('graphics/lamp.png').convert_alpha()
water = pygame.image.load('graphics/water.png').convert_alpha()

#INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,180,3)
player_stand_rect = player_stand.get_rect(center = (500,300))
game_name = test_font.render('Dr.Fart! You\'re needed at the Hospital ASAP!', False,(64,64,64))
game_name_rect = game_name.get_rect(center = (500,100))
game_message = test_font.render('Press SPACE and scurry on to the Hospital', False, (64,64,64))
game_message_rect = game_message.get_rect(center = (500,500))

#TIMER
x = 1200  
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, x)

bd_1_width = buildings_1.get_width()
b1_scroll = 0
b1_tiles = math.ceil(screen_width / bd_1_width) + 1

bd_2_width = buildings_2.get_width()
b2_scroll = 0
b2_tiles = math.ceil(screen_width / bd_2_width) + 1

bd_3_width = buildings_3.get_width()
b3_scroll = 0
b3_tiles = math.ceil(screen_width / bd_3_width) + 1

lamp_width = lamp.get_width()
lamp_scroll = 0
lamp_tiles = math.ceil(screen_width / lamp_width) + 1

water_width = water.get_width()
water_scroll = 0
water_tiles = math.ceil(screen_width / water_width) + 1

ground_width = ground.get_width()
ground_scroll = 0
ground_tiles = math.ceil(screen_width / ground_width) + 1

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:     
            if event.type == obstacle_timer:
              obstacle_group.add(Obstacle(choice(['flying','flying','ground','ground','ground'])))   
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

# While game is active
    if game_active:
        bg_music.set_volume(0.5)
        screen.blit(sky_surface, (0,0))
        # Buildings
        for i in range(0, b3_tiles):
            screen.blit(buildings_3, (i * bd_3_width + b3_scroll,100))
        b3_scroll -= 0.2
        if abs(b3_scroll) > bd_3_width:
            b3_scroll = 0  
       
        for i in range(0, b2_tiles):
            screen.blit(buildings_2, (i * bd_2_width + b2_scroll,80))
        b2_scroll -= 0.3
        if abs(b2_scroll) > bd_2_width:
            b2_scroll = 0   

        for i in range(0, b1_tiles):
            screen.blit(buildings_1, (i * bd_1_width + b1_scroll,10))
        b1_scroll -= 0.4
        if abs(b1_scroll) > bd_1_width:
            b1_scroll = 0

        for i in range(0, lamp_tiles):
            screen.blit(lamp, (i * lamp_width + lamp_scroll,300))
        lamp_scroll -= 2
        if abs(lamp_scroll) > lamp_width:
            lamp_scroll = 0         

        # screen.blit(ground_surface, (0,500))
        for i in range(0, ground_tiles):
            screen.blit(ground, (i * ground_width + ground_scroll,500))
        ground_scroll -= 2
        if abs(ground_scroll) > ground_width:
            ground_scroll = 0 
            
        for i in range(0, water_tiles):
            screen.blit(water, (i * water_width + water_scroll,490))
        water_scroll -= 3
        if abs(water_scroll) > water_width:
            water_scroll = 0  

        # Clouds
        clouds_x_pos -= 0.1
        if clouds_x_pos <-500: clouds_x_pos = 1000
        screen.blit(clouds_surface, (clouds_x_pos,-40))
        clouds_x1_pos -= 0.1
        if clouds_x1_pos <-500: clouds_x1_pos = 1000
        screen.blit(clouds_surface, (clouds_x1_pos,-20))

        score = display_score_bg()
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        game_message = display_message()

        
# While game is not active        
    else:
        bg_music.set_volume(0.1)
        screen.fill((255,183,197))
        screen.blit(player_stand,player_stand_rect)
        
        score_message = test_font.render(f'Only {score}? Your patients are DEAD. ', False, (0,0,0))
        score_message_rect = score_message.get_rect(center = (500,300))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)

        else: 
            screen.fill((234, 60, 83))
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)
    
