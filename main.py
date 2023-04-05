# Import Libraries
import pygame as pg
import random

# Initialize Game
pg.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# Clock 
clock = pg.time.Clock()
FPS = 60

# Game Variables
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESHOLD = 200
scroll = bg_scroll = score = fade_counter = 0

game_over = False

# Define Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

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

# Function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image,(0,0+bg_scroll))
    screen.blit(bg_image,(0,-600+bg_scroll))

# Function for outputting text on to the screen
def draw_text(text,font,text_color,x,y):
    img = font.render(text,True,text_color)
    screen.blit(source=img, dest=(x,y))

# Platform Class
class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):
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


        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESHOLD:
            # if player is jumping
            if self.y_velocity<0:
                scroll =-dy

        # Update rectangle position
        self.rect.x+=dx
        self.rect.y+=dy+scroll

        return scroll

# player instance
performer = Performer(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-150)

# sprite group
platform_group = pg.sprite.Group()

# starting platform
platform = Platform(x=SCREEN_WIDTH//2 - 50, y=SCREEN_HEIGHT-50, width=100)
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
            platform = Platform(x=platform_x,y=platform_y,width=platform_width)
            platform_group.add(platform)



        # Draw Platforms
        platform_group.draw(screen)

        # Update Platform
        platform_group.update(scroll=scroll)

        # Draw Performer
        performer.draw()

        # Check game over
        if performer.rect.top > SCREEN_HEIGHT:
            game_over=True

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter+=5
            for y in range(0,6,2):
                pg.draw.rect(surface=screen,color=BLACK,rect=(0,y*100,fade_counter,SCREEN_HEIGHT/6))
                pg.draw.rect(surface=screen,color=BLACK,rect=(SCREEN_WIDTH-fade_counter,(y+1)*100,SCREEN_WIDTH,SCREEN_HEIGHT/6))
        draw_text(text="Game Over!", font=font_big, text_color=WHITE, x=130, y=200)
        draw_text(text="Score: "+str(score), font=font_small, text_color=WHITE, x=150, y=250)
        draw_text(text="Press space to play again!", font=font_big, text_color=WHITE, x=40, y=300)

        # Looking for space bar being pressed

        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            
            # Reset variables 
            game_over = False
            score = scroll = fade_counter = 0 
            
            # Reposition Performer
            performer.rect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT-150)

            # Reset Platforms
            platform_group.empty()

            # starting platform
            platform = Platform(x=SCREEN_WIDTH//2 - 50, y=SCREEN_HEIGHT-50, width=100)
            platform_group.add(platform)


    # Event handler
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run=False

    # Update Display Window
    pg.display.update()

pg.quit()