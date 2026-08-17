import pygame

MAX_HEALTH = 10
HEART_SIZE = 18
HEART_GAP = 5


def update_arrows(arrow_list, maze_walls, player1, player2):
    # Moves arrows and handles:
    # Arrow disappearing when it hits a maze wall
    # Arrow disappearing when it hits a player
    # Player health damage
    # Detecting Game Over

    for arrow in arrow_list[:]:
        arrow.update()

        # Arrow disappears immediately when it hits a maze wall
        hit_wall = False

        for wall in maze_walls:
            if arrow.rect.colliderect(wall):
                arrow_list.remove(arrow)
                hit_wall = True
                break

        if hit_wall:
            continue

        # Remove arrows that leave the screen
        if (arrow.rect.right < 0 or arrow.rect.left > 800 or
                arrow.rect.bottom < 0 or arrow.rect.top > 600):
            arrow_list.remove(arrow)
            continue

        # Player 1's arrow hits Player 2
        if arrow.shooter_num == 1 and player2.health > 0:
            if arrow.rect.colliderect(player2.rect):
                player2.health = max(0, player2.health - arrow.damage)
                arrow_list.remove(arrow)

        # Player 2's arrow hits Player 1
        elif arrow.shooter_num == 2 and player1.health > 0:
            if arrow.rect.colliderect(player1.rect):
                player1.health = max(0, player1.health - arrow.damage)
                arrow_list.remove(arrow)

    # Game Over if either player reaches 0 health
    return player1.health <= 0 or player2.health <= 0


def update_players(player1, player2, arrow_list):

   # Updates both players.

   # Dead players cannot move, charge their bow, or shoot arrows.
    

    # Player 1
    if player1.health > 0:
        player1.update(arrow_list)
    else:
        # Stop Player 1 from shooting after death
        player1.is_charging = False
        player1.charge_frame = 0
        player1.is_moving = False

    # Player 2
    if player2.health > 0:
        player2.update(arrow_list)
    else:
        # Stop Player 2 from shooting after death
        player2.is_charging = False
        player2.charge_frame = 0
        player2.is_moving = False


def draw_hearts(screen, player, x, y, player_name):
    # Draws one heart for each health point

    font = pygame.font.Font(None, 26)

    label = font.render(
        player_name,
        True,
        (255, 255, 255)
    )

    screen.blit(label, (x, y - 25))

    for i in range(MAX_HEALTH):
        heart_x = x + i * (HEART_SIZE + HEART_GAP)

        if i < player.health:
            draw_heart(
                screen,
                heart_x,
                y,
                HEART_SIZE,
                True
            )
        else:
            draw_heart(
                screen,
                heart_x,
                y,
                HEART_SIZE,
                False
            )


def draw_heart(screen, x, y, size, filled=True):
    # Draws a heart without requiring another image file

    if filled:
        color = (255, 50, 70)
    else:
        color = (70, 70, 70)

    half = size // 2

    # Left side of heart
    pygame.draw.circle(
        screen,
        color,
        (x + half // 2, y + half // 2),
        half // 2
    )

    # Right side of heart
    pygame.draw.circle(
        screen,
        color,
        (x + half + half // 2, y + half // 2),
        half // 2
    )

    # Bottom of heart
    pygame.draw.polygon(
        screen,
        color,
        [
            (x + 1, y + half // 2),
            (x + size - 1, y + half // 2),
            (x + half, y + size)
        ]
    )


def draw_game_over(screen, player1, player2):
    #Displays the Game Over screen

    overlay = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 80)
    info_font = pygame.font.Font(None, 38)

    # GAME OVER title
    title = title_font.render(
        "GAME OVER",
        True,
        (255, 255, 255)
    )

    title_rect = title.get_rect(
        center=(
            screen.get_width() // 2,
            220
        )
    )

    screen.blit(title, title_rect)

    # Determine winner
    if player1.health <= 0 and player2.health <= 0:
        result = "Draw!"
    elif player1.health <= 0:
        result = "Player 2 Wins!"
    else:
        result = "Player 1 Wins!"

    result_text = info_font.render(
        result,
        True,
        (255, 255, 255)
    )

    result_rect = result_text.get_rect(
        center=(
            screen.get_width() // 2,
            300
        )
    )

    screen.blit(result_text, result_rect)

    # Quit message
    hint = info_font.render(
        "Press ESC to quit",
        True,
        (220, 220, 220)
    )

    hint_rect = hint.get_rect(
        center=(
            screen.get_width() // 2,
            360
        )
    )

    screen.blit(hint, hint_rect)


def game_over_event(event):
#Returns True if ESC is pressed on the Game Over screen

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

    return False
