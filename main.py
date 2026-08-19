import pygame
import players 
import archery
import menu

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
pygame.display.set_caption("Untitled Archery Game")
clock = pygame.time.Clock()

themenu = menu.Menu(WIDTH, HEIGHT)
p1 = players.Player(100, 300, player_num=1)
p2 = players.Player(600, 300, player_num=2)
arrow_list = []
maze_walls = []
is_game_over = archery.update_arrows(arrow_list, maze_walls, p1, p2)

running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        themenu.handle_event(event)

        if is_game_over and archery.game_over_event(event):
            running = False

        if is_game_over and archery.game_over_event(event):
            running = False

    if themenu.currentstate == "start":
        if not is_game_over:
            p1.update(arrow_list)
            p2.update(arrow_list)
            is_game_over = archery.update_arrows(arrow_list, maze_walls, p1, p2)

        screen.fill(color=BLUE)
        p1.draw(screen)
        p2.draw(screen) 

        p1.update(arrow_list)
        p2.update(arrow_list)

        for arrow in arrow_list:
            arrow.draw(screen)

        archery.update_arrows(arrow_list, maze_walls, p1, p2)
        archery.draw_hearts(screen, p1, 20, 35, "Player 1")
        archery.draw_hearts(screen, p2, 450, 35, "Player 2")

        if is_game_over:
            archery.draw_game_over(screen, p1, p2)

    else:
        themenu.draw(screen, mouse_pos)   
    pygame.display.flip()
pygame.quit()