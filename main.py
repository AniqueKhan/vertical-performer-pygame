# Import Libraries
import pygame as pg
import random

# Initialize Game
pg.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# Clock 
clock = pg.time.Clock()
FPS=60

# Game Variables
GRAVITY = 1
MAX_PLATFORMS = 10

# Define Colors
WHITE = (255,255,255)

# Create Game Window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Vertical Performer - Anique")

# Load Images
bg_image = pg.image.load('assets/bg.png').convert_alpha()
performer_image =pg.transform.scale(pg.image.load('assets/performer.png').convert_alpha(),(45,45))
platform_image =pg.transform.scale(pg.image.load('assets/wood.png').convert_alpha(),(45,45))


# Platform Class
class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        dx,dy=0,0

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

        # check collision with ground
        if self.rect.bottom +dy>SCREEN_HEIGHT:
            dy=0 
            self.y_velocity=-20

        # Update rectangle position
        self.rect.x+=dx
        self.rect.y+=dy

# player instance
performer = Performer(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-150)

# sprite group
platform_group = pg.sprite.Group()

# temporary platforms
for p in range(MAX_PLATFORMS):
    platform_width = random.randint(40,60)
    platform_x = random.randint(0,SCREEN_WIDTH-platform_width)
    platform_y = p*random.randint(80,120)
    platform = Platform(x=platform_x, y=platform_y, width=platform_width)
    platform_group.add(platform)

# Game Loop
run = True
while run:
    clock.tick(FPS)

    # Move Performer
    performer.move()

    # Draw Background
    screen.blit(source=bg_image, dest=(0,0))

    # Draw Platforms
    platform_group.draw(screen)

    # Draw Performer
    performer.draw()

    # Event handler
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run=False

    # Update Display Window
    pg.display.update()

pg.quit()