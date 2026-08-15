import pygame
<<<<<<< HEAD
import player
=======
import players
>>>>>>> players

# Make constants
WIDTH = 800
HEIGHT = 600
FPS = 30
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init() # sounds
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

<<<<<<< HEAD
theplayer = player.Player(100,100)
=======
p1 = players.Player(100, 300, player_num=1)
p2 = players.Player(600, 300, player_num=2)
arrow_list = []
>>>>>>> players

running = True
while running:
    # Clock
    clock.tick(FPS)
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Drawing
    p1.update(arrow_list)
    p2.update(arrow_list)

    screen.fill(color=BLUE) # drawing the background
<<<<<<< HEAD
    theplayer.draw(screen)
=======
    p1.draw(screen)
    p2.draw(screen) 
>>>>>>> players
    
    pygame.display.flip()
# quit the game after the loop exits
pygame.quit()