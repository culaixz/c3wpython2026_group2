import pygame
import players

# Make constants
WIDTH = 720
HEIGHT = 720
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
player = players.Player(200,100)
running = True
while running:
    # Clock
    clock.tick(FPS)
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Drawing
    player.update()

    screen.fill(color=BLUE)
    player.draw(screen) # drawing the background
    
    pygame.display.flip()
# quit the game after the loop exits
pygame.quit()