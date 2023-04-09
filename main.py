# Import Libraries
import pygame as pg
import random
import os

# Initialize Game
pg.init()
pg.mixer.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# Animation constant
ANIMATION_COOLDOWN = 50

# Clock 
clock = pg.time.Clock()
FPS = 60

# Load Music and Sounds
pg.mixer.music.load('assets/music.mp3')
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(-1,0.0,5000)

jump_fx = pg.mixer.Sound('assets/jump.mp3')
jump_fx.set_volume(0.5)

death_fx = pg.mixer.Sound('assets/death.mp3')
death_fx.set_volume(0.5)

# Game Variables
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESHOLD = 200
scroll = bg_scroll = score = fade_counter = 0
game_over = False

# Read High Score From score.txt
if os.path.exists("score.txt"):
    with open('score.txt','r') as file:
        high_score = int(file.read())
else:
    high_score=0

# Define Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
PANEL = (153,217,234)

# Define Font
font_small = pg.font.SysFont(name="Lucida Sans", size=20)
font_big = pg.font.SysFont(name="Lucida Sans", size=24)

# Create Game Window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Vertical Performer - Anique")

# Load Images
bg_image = pg.image.load('assets/bg.png').convert_alpha()
performer_image =pg.transform.scale(pg.image.load('assets/performer.png').convert_alpha(),(45,45))
platform_image =pg.transform.scale(pg.image.load('assets/wood.png').convert_alpha(),(45,45))

# Bird Spritesheet
bird_image = pg.image.load('assets/bird.png').convert_alpha()

# Function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image,(0,0+bg_scroll))
    screen.blit(bg_image,(0,-600+bg_scroll))

# Function for outputting text on to the screen
def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(source=img, dest=(x,y))

# Function for drawing info panel
def draw_panel():
    pg.draw.rect(surface=screen,color=PANEL,rect=(0,0,SCREEN_WIDTH,30))
    pg.draw.line(surface=screen,color=WHITE,start_pos=(0,30),end_pos=(SCREEN_WIDTH,30),width=2)
    draw_text(text="SCORE: "+str(score), font=font_small, text_color=WHITE, x=0, y=0)
    draw_text(text="HIGH SCORE: "+str(high_score), font=font_small, text_color=WHITE, x=SCREEN_WIDTH-200, y=0)

# Helper Class
class Spritesheet():
    def __init__(self,image):
        self.sheet = image

    def get_image(self,frame,width,height,scale,color):
        image = pg.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),((frame*width),0,width,height))
        image = pg.transform.scale(image,(int(width*scale),(int(height*scale))))
        image.set_colorkey(color)
        return image

bird_sheet = Spritesheet(bird_image)

class Enemy(pg.sprite.Sprite):
    def __init__(self,y,sprite_sheet,scale):
        pg.sprite.Sprite.__init__(self)
        self.direction = random.choice([-1,1])
        self.flip = True if self.direction == 1 else False
        self.animation_list , self.frame_index , self.update_time = [] , 0 , pg.time.get_ticks()

        # Load Images From Spritesheet
        animation_steps = 8
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(frame=animation,width=32,height=32,scale=scale,color=(0,0,0))
            image = pg.transform.flip(image,self.flip,False)
            image.set_colorkey((0,0,0))
            self.animation_list.append(image)

        # Select Starting Image and Create Rectangle From It
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        
        self.rect.x = 0 if self.direction == 1 else SCREEN_WIDTH
        self.rect.y = y
        
        

    def update(self):
        # update animation
        self.image = self.animation_list[self.frame_index]

        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index+=1
            self.update_time=pg.time.get_ticks()

        # if the animation has run out then reset back to the start
        if self.frame_index>=len(self.animation_list):
            self.frame_index=0

        # move enemy horizontally
        self.rect.x+=self.direction*2
        self.rect.y+=scroll

        # check if gone off screen
        if self.rect.right <0 or self.rect.left>SCREEN_WIDTH:
            self.kill()


# Platform Class
class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,width,moving):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.move_counter = random.randint(a=0, b=50)
        self.direction = random.choice([-1,1])
        self.speed = random.randint(a=1, b=2)

    def update(self,scroll):
        # move platforms horizontally
        if self.moving:
            self.move_counter+=1
            self.rect.x+=self.direction*self.speed

        # change platform direction if it has moved fully or hit a wall
        if self.move_counter>=100 or self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.direction*=-1
            self.move_counter=0
        
        # update platform's vertical position
        self.rect.y+=scroll

        # check if platform has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Performer Class
class Performer():
    def __init__(self,x,y):
        self.image = performer_image
        self.width , self.height = 25 , 40
        self.rect = pg.Rect(0,0,self.width,self.height)
        self.rect.center = (x,y)
        self.flip=False
        self.y_velocity = 0

    def draw(self):
        screen.blit(pg.transform.flip(self.image,self.flip,False),(self.rect.x-12,self.rect.y-5))
        # pg.draw.rect(screen,WHITE,self.rect,2)

    def move(self):
        # reset variables
        dx,dy,scroll=0,0,0

        # key presses
        key = pg.key.get_pressed()

        if key[pg.K_a]:
            dx=-10
            self.flip = True
        if key[pg.K_d]:
            dx=10
            self.flip=False

        # gravity
        self.y_velocity+=GRAVITY
        dy+=self.y_velocity

        # ensure that the player does not go off the screen
        if self.rect.left + dx < 0:
            dx=-self.rect.left

        if self.rect.right +dx > SCREEN_WIDTH:
            dx=SCREEN_WIDTH-self.rect.right

        # check collision with platforms
        for platform in platform_group:
            # collision in the y-direction
            if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                # check if above the platform
                if self.rect.bottom<platform.rect.centery:
                    if self.y_velocity>0:
                        self.rect.bottom = platform.rect.top
                        dy=0
                        self.y_velocity=-20
                        # play jump sound
                        jump_fx.play()


        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESHOLD:
            # if player is jumping
            if self.y_velocity<0:
                scroll =-dy

        # Update rectangle position
        self.rect.x+=dx
        self.rect.y+=dy+scroll

        # Create mask for better collision scenarios
        self.mask = pg.mask.from_surface(self.image)

        return scroll

# player instance
performer = Performer(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-150)

# sprite group
platform_group =  pg.sprite.Group()
enemy_group = pg.sprite.Group()

# starting platform
platform = Platform(x=SCREEN_WIDTH//2 - 50, y=SCREEN_HEIGHT-50, width=100,moving=False)
platform_group.add(platform)

# Game Loop
run = True
while run:
    clock.tick(FPS)

    if not game_over:

        # Move Performer
        scroll = performer.move()

        # Draw Background
        bg_scroll+=scroll
        
        if bg_scroll >=600:
            bg_scroll=0

        draw_bg(bg_scroll=bg_scroll)

        # Generate platforms
        if len(platform_group)<MAX_PLATFORMS:
            platform_width = random.randint(a=40, b=60)
            platform_x = random.randint(a=0, b=SCREEN_WIDTH-platform_width)
            platform_y=platform.rect.y-random.randint(a=80, b=120)
            platform_type = random.randint(1, 2)
            if platform_type == 1 and score >500:
                platform_moving = True
            else:
                platform_moving=False
            platform = Platform(x=platform_x,y=platform_y,width=platform_width,moving=platform_moving)
            platform_group.add(platform)

        # Draw Platforms
        platform_group.draw(screen)

        # Update Platform
        platform_group.update(scroll=scroll)

        # Generate Enemies
        if len(enemy_group)==0 and score > 1000:
            enemy = Enemy(y=100, sprite_sheet=bird_sheet, scale=1.5)
            enemy_group.add(enemy)

        # Draw Enemies
        enemy_group.draw(screen)

        # Update Enemies
        enemy_group.update()

        # Update Score
        if scroll > 0:
            score+=scroll

        # Draw line at previous high score
        pg.draw.line(surface=screen,color=WHITE,start_pos=(0,score-high_score+SCROLL_THRESHOLD),end_pos=(SCREEN_WIDTH,score-high_score+SCROLL_THRESHOLD),width=3)
        draw_text(text="HIGH SCORE", font=font_small, text_color=WHITE, x=SCREEN_WIDTH-130, y=score-high_score+SCROLL_THRESHOLD)
        
        # Draw Performer
        performer.draw()

        # Draw Panel
        draw_panel()

        # Check game over
        if performer.rect.top > SCREEN_HEIGHT:
            game_over=True
            death_fx.play()
        
        # Check for collision with enemies
        # Nesting the collision without the mask in order to make the computation faster
        if pg.sprite.spritecollide(sprite=performer, group=enemy_group, dokill=False):
            if pg.sprite.spritecollide(sprite=performer,group=enemy_group,dokill=False,collided=pg.sprite.collide_mask):
                game_over=True
                death_fx.play()

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter+=5
            for y in range(0,6,2):
                pg.draw.rect(surface=screen,color=BLACK,rect=(0,y*100,fade_counter,SCREEN_HEIGHT/6))
                pg.draw.rect(surface=screen,color=BLACK,rect=(SCREEN_WIDTH-fade_counter,(y+1)*100,SCREEN_WIDTH,SCREEN_HEIGHT/6))
        else:
            draw_text(text="Game Over!", font=font_big, text_color=WHITE, x=130, y=200)
            draw_text(text="Score: "+str(score), font=font_small, text_color=WHITE, x=150, y=250)
            draw_text(text="Press space to play again!", font=font_big, text_color=WHITE, x=40, y=300)

            # Update high score
            if score>high_score:
                high_score=score
                with open("score.txt","w") as file:
                    file.write(str(high_score))

            # Looking for space bar being pressed

            key = pg.key.get_pressed()
            if key[pg.K_SPACE]:
                
                # Reset variables 
                game_over = False
                score = scroll = fade_counter = 0 
                
                # Reposition Performer
                performer.rect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT-150)
                
                # Reset Enemies
                enemy_group.empty()

                # Reset Platforms
                platform_group.empty()

                # starting platform
                platform = Platform(x=SCREEN_WIDTH//2 - 50, y=SCREEN_HEIGHT-50, width=100,moving=False)
                platform_group.add(platform)


    # Event handler
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run=False

    # Update Display Window
    pg.display.update()

pg.quit()