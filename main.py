import pygame
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
running = True
while running:
    # Clock
    clock.tick(FPS)
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Drawing
    screen.fill(color=BLUE) # drawing the background
    
    pygame.display.flip()
# quit the game after the loop exits
pygame.quit()