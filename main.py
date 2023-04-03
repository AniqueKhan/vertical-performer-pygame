# Import Libraries
import pygame as pg

# Initialize Game
pg.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# Clock 
clock = pg.time.Clock()
FPS=60

# Define Colors
WHITE = (255,255,255)

# Create Game Window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Vertical Performer - Anique")

# Load Images
bg_image = pg.image.load('assets/bg.png').convert_alpha()
performer_image =pg.transform.scale(pg.image.load('assets/performer.png').convert_alpha(),(45,45))


# Performer Class
class Performer():
    def __init__(self,x,y):
        self.image = performer_image
        self.width , self.height = 25 , 40
        self.rect = pg.Rect(0,0,self.width,self.height)
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.image,(self.rect.x-12,self.rect.y-5))
        # pg.draw.rect(screen,WHITE,self.rect,2)

    def move(self):
        # key presses
        key = pg.key.get_pressed()

        if key[pg.K_a]:
            self.rect.x-=10
        if key[pg.K_d]:
            self.rect.x+=10

performer = Performer(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-150)



# Game Loop
run = True
while run:
    clock.tick(FPS  )

    # Move Performer
    performer.move()

    # Draw Background
    screen.blit(source=bg_image, dest=(0,0))

    # Draw Performer
    performer.draw()

    # Event handler
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
            run=False

    # Update Display Window
    pg.display.update()

pg.quit()