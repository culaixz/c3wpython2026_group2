import pygame
import sys
import players 
import archery
import menu
import Collision 
import audio


WIDTH = 800  
HEIGHT = 600
FPS = 60 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
music_player = audio.AudioManager()
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Arena")
clock = pygame.time.Clock()

if hasattr(Collision, 'Background') and Collision.Background is not None:
    background_img = Collision.Background
else:
    try:
        background_img = pygame.image.load("NewestBGS.png").convert_alpha()
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    except pygame.error:
        background_img = None

# Initialize Class Instances 
themenu = menu.Menu(WIDTH, HEIGHT)
p1 = players.Player(25, -4, player_num=1)     
p2 = players.Player(705, 495, player_num=2)   
arrow_list = []                                
maze_walls = Collision.maze_walls              
is_game_over = False

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

    if themenu.currentstate == "start":
        music_player.play_gameplay_music()

        if not is_game_over:

            p1_old_x, p1_old_y = p1.pos.x, p1.pos.y
            p2_old_x, p2_old_y = p2.pos.x, p2.pos.y

            p1.update(arrow_list)
            p2.update(arrow_list)

            p1.rect.x = int(p1.pos.x)
            p1.feet_rect.x = int(p1.pos.x)
            for item in maze_walls:
                if p1.feet_rect.colliderect(item.rect):
                    p1.pos.x = p1_old_x
                    p1.feet_rect.x = int(p1_old_x)
                    p1.rect.x = int(p1_old_x)
                    break

            p1.rect.y = int(p1.pos.y)
            p1.feet_rect.y = int(p1.pos.y + 24)
            for item in maze_walls:
                if p1.feet_rect.colliderect(item.rect):
                    p1.pos.y = p1_old_y
                    p1.feet_rect.y = int(p1_old_y + 24)
                    p1.rect.y = int(p1_old_y)
                    break

            p2.rect.x = int(p2.pos.x)
            p2.feet_rect.x = int(p2.pos.x)
            for item in maze_walls:
                if p2.feet_rect.colliderect(item.rect):
                    p2.pos.x = p2_old_x
                    p2.feet_rect.x = int(p2_old_x)
                    p2.rect.x = int(p2_old_x)
                    break

            p2.rect.y = int(p2.pos.y)
            p2.feet_rect.y = int(p2.pos.y + 24)
            for item in maze_walls:
                if p2.feet_rect.colliderect(item.rect):
                    p2.pos.y = p2_old_y
                    p2.feet_rect.y = int(p2_old_y + 24)
                    p2.rect.y = int(p2_old_y)
                    break

            is_game_over = archery.update_arrows(arrow_list, maze_walls, p1, p2)

        if background_img is not None:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill((25, 25, 112))
            pygame.draw.rect(screen, (34, 139, 34), (0, 500, 800, 100))

        # Optional Pink Hitbox Trace Layout (Uncomment to inspect map structures)
        #for item in maze_walls:
            #pygame.draw.rect(screen, (255, 0, 255), item.rect, 2)

        for arrow in arrow_list:
            arrow.draw(screen)

        if p1.health > 0: p1.draw(screen)
        if p2.health > 0: p2.draw(screen) 

        archery.draw_hearts(screen, p1, 20, 35, "Player 1")
        archery.draw_hearts(screen, p2, 450, 35, "Player 2")

        if is_game_over:
            music_player.stop_music()
            archery.draw_game_over(screen, p1, p2)

    else:
        music_player.play_menu_music()
        themenu.draw(screen, mouse_pos)   

    pygame.display.flip()

pygame.quit()
sys.exit()

