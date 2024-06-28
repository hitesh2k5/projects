import pygame
import sys
import random
import time

# Game settings
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 10
CELL_SIZE = WIDTH // BOARD_SIZE
MARGIN = 50
DICE_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]

# Initialize Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH + MARGIN * 2, HEIGHT + MARGIN * 2 + DICE_SIZE + 20))
pygame.display.set_caption("Snake and Ladder Game")

# Dice settings
dice_value = 1
dice_pos = (WIDTH // 2 + MARGIN - DICE_SIZE // 2, HEIGHT + MARGIN + 10)

# Player positions (starting from position 100)
player_positions = []
player_index = 0
is_moving = False  # Flag to indicate if a player is currently moving

# Snakes and Ladders mapping (reversed for descending movement)
snakes = {6: 16, 26: 47, 11: 49, 53: 56, 19: 62, 60: 64, 24: 87, 73: 93, 75: 95, 78: 98}
ladders = {38: 1, 14: 4, 31: 9, 42: 21, 84: 28, 44: 36, 67: 51, 91: 71, 100: 80}

# Roll the dice
def roll_dice():
    return random.randint(1, 6)

# Convert board position to screen coordinates
def position_to_coords(position):
    row = (position - 1) // BOARD_SIZE
    col = (position - 1) % BOARD_SIZE
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col
    x = col * CELL_SIZE + MARGIN
    y = HEIGHT - (row + 1) * CELL_SIZE + MARGIN
    return x + CELL_SIZE // 2, y + CELL_SIZE // 2

# Draw the board
def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            num = row * BOARD_SIZE + col + 1
            if row % 2 == 1:
                num = row * BOARD_SIZE + (BOARD_SIZE - 1 - col) + 1
            pygame.draw.rect(screen, WHITE if (row + col) % 2 == 0 else BLACK, (col * CELL_SIZE + MARGIN, row * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
            font = pygame.font.Font(None, 24)
            text = font.render(str(num), True, BLACK if (row + col) % 2 == 0 else WHITE)
            text_rect = text.get_rect(center=(col * CELL_SIZE + MARGIN + CELL_SIZE // 2, row * CELL_SIZE + MARGIN + CELL_SIZE // 2))
            screen.blit(text, text_rect)
    
    # Draw snakes
    for head, tail in snakes.items():
        pygame.draw.line(screen, RED, position_to_coords(head), position_to_coords(tail), 5)
    
    # Draw ladders
    for bottom, top in ladders.items():
        pygame.draw.line(screen, GREEN, position_to_coords(bottom), position_to_coords(top), 5)
    
    # Draw the dice
    pygame.draw.rect(screen, BLACK, (*dice_pos, DICE_SIZE, DICE_SIZE), border_radius=10)
    font = pygame.font.Font(None, 36)
    text = font.render(str(dice_value), True, WHITE)
    text_rect = text.get_rect(center=(dice_pos[0] + DICE_SIZE // 2, dice_pos[1] + DICE_SIZE // 2))
    screen.blit(text, text_rect)

    # Draw the players
    for idx, pos in enumerate(player_positions):
        player_coords = position_to_coords(pos)
        pygame.draw.circle(screen, PLAYER_COLORS[idx], player_coords, CELL_SIZE // 4)

    pygame.display.flip()

def move_player(player_idx, steps):
    global player_positions, is_moving
    is_moving = True
    start_position = player_positions[player_idx]
    target_position = start_position - steps

    for pos in range(start_position - 1, target_position - 1, -1):
        player_positions[player_idx] = pos
        if player_positions[player_idx] < 1:
            player_positions[player_idx] = 1
            break
        draw_board()
        time.sleep(0.2)
    
    # Apply snakes or ladders after moving
    if player_positions[player_idx] in snakes:
        player_positions[player_idx] = snakes[player_positions[player_idx]]
    elif player_positions[player_idx] in ladders:
        player_positions[player_idx] = ladders[player_positions[player_idx]]
    
    draw_board()
    is_moving = False

def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render("Snake and Ladder", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 + MARGIN, HEIGHT // 4))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Select Number of Players", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 + MARGIN, HEIGHT // 2))
    screen.blit(text, text_rect)

    for i in range(2, 5):
        text = font.render(str(i), True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2 + MARGIN - 100 + 100 * (i - 2), HEIGHT // 2 + 50))
        screen.blit(text, text_rect)

    pygame.display.flip()

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(2, 5):
                    text_rect = pygame.Rect(WIDTH // 2 + MARGIN - 100 + 100 * (i - 2) - 20, HEIGHT // 2 + 50 - 20, 40, 40)
                    if text_rect.collidepoint(event.pos):
                        return i

def main():
    global dice_value, player_index, is_moving
    num_players = show_start_screen()
    for _ in range(num_players):
        player_positions.append(100)  # Start each player at position 100
    
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_moving:
                if pygame.Rect(*dice_pos, DICE_SIZE, DICE_SIZE).collidepoint(event.pos):
                    for _ in range(10):
                        dice_value = roll_dice()
                        draw_board()
                        pygame.time.wait(100)
                    dice_value = roll_dice()
                    move_player(player_index, dice_value)
                    if player_positions[player_index] == 1:
                        game_over = True
                        break
                    player_index = (player_index + 1) % num_players
                    draw_board()

        draw_board()
        clock.tick(30)

    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render(f"Player {player_index + 1} Wins!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 + MARGIN, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(3)

if __name__ == "__main__":
    main()
