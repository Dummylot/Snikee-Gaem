import pygame
import random


# Initialize Pygame
pygame.init()

# Define constants
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 16
WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BUH = (1, 46, 0)
GOLD = (255, 215, 0)  # Golden color for the golden apple

# Set up the display
nut = pygame.image.load("GoldenApple.png")
nut = pygame.transform.scale(nut, (GRID_SIZE, GRID_SIZE))  # Scale to grid size

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Gaem')
pygame.display.set_icon(nut)

# Load apple sprite and golden apple sprite
apple_sprite = pygame.image.load("Apple.png")
apple_sprite = pygame.transform.scale(apple_sprite, (GRID_SIZE, GRID_SIZE))  # Scale to grid size

golden_apple_sprite = pygame.image.load("GoldenApple.png")  # Make sure you have a golden apple image
golden_apple_sprite = pygame.transform.scale(golden_apple_sprite, (GRID_SIZE, GRID_SIZE))

# Load background image (cloud.jpg)
background = pygame.image.load("cloud.jpg")  # Ensure you have a "cloud.jpg" file in the working directory
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to fit the screen size

# Define the snake
snake = {
    "x": 160,
    "y": 160,
    "dx": GRID_SIZE,
    "dy": 0,
    "body": [(160, 160)],
    "max_length": 4,
    "color": GREEN  # Default snake color
}

# Define the apple
apple = {
    "x": random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
    "y": random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
    "is_gold": False  # Whether the apple is golden or not
}

# Set up the clock
clock = pygame.time.Clock()

# Variables for the shop menu
shop_open = False
snake_colors = [GREEN, RED, (255, 255, 0), (0, 0, 255)]  # Predefined color options
current_color = 0  # Index of the current snake color

# Score variable
score = 0

# Function to reset the game
def reset_game():
    global score  # Reset the score when restarting the game
    score = 0
    snake["x"] = 160
    snake["y"] = 160
    snake["dx"] = GRID_SIZE
    snake["dy"] = 0
    snake["body"] = [(160, 160)]
    snake["max_length"] = 4
    apple["x"] = random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE
    apple["y"] = random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
    apple["is_gold"] = random.random() < 0.43  # 43% chance to spawn a golden apple

# Function to display the score
def display_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the game over screen
def game_over():
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("'R' to Restart", True, WHITE)

    screen.blit(background, (0, 0))  # Blit the background before everything else
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 4 - 50))
    screen.blit(score_text, (WIDTH // 4, HEIGHT // 4))
    screen.blit(restart_text, (WIDTH // 4, HEIGHT // 4 + 50))

    pygame.display.flip()

# Main game loop
running = True
game_active = True  # Game state variable

while running:
    # Blit the background first
    screen.blit(background, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Open/close the shop with Q
                shop_open = not shop_open
            if event.key == pygame.K_r and not game_active:  # Restart the game with 'R'
                game_active = True
                reset_game()
            if event.key == pygame.K_q and not game_active:  # Quit the game with 'Q'
                running = False
            if shop_open:
                if event.key == pygame.K_UP:  # Move up in the color list
                    current_color = (current_color - 1) % len(snake_colors)
                if event.key == pygame.K_DOWN:  # Move down in the color list
                    current_color = (current_color + 1) % len(snake_colors)
                if event.key == pygame.K_RETURN:  # Confirm color selection
                    snake["color"] = snake_colors[current_color]
                    shop_open = False  # Close the shop menu

    # If the game is active, handle movement and other logic
    if game_active:
        # Handle snake movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake["dx"] == 0:
            snake["dx"], snake["dy"] = -GRID_SIZE, 0
        if keys[pygame.K_UP] and snake["dy"] == 0:
            snake["dx"], snake["dy"] = 0, -GRID_SIZE
        if keys[pygame.K_RIGHT] and snake["dx"] == 0:
            snake["dx"], snake["dy"] = GRID_SIZE, 0
        if keys[pygame.K_DOWN] and snake["dy"] == 0:
            snake["dx"], snake["dy"] = 0, GRID_SIZE

        # Update snake position
        snake["x"] += snake["dx"]
        snake["y"] += snake["dy"]

        # Wrap snake position
        snake["x"] %= WIDTH
        snake["y"] %= HEIGHT

        # Add new position to the snake's body
        snake["body"].insert(0, (snake["x"], snake["y"]))

        # Trim the snake's body to the max length
        if len(snake["body"]) > snake["max_length"]:
            snake["body"].pop()

        # Check for collisions with the apple
        if snake["x"] == apple["x"] and snake["y"] == apple["y"]:
            snake["max_length"] += 1
            if apple["is_gold"]:
                score += 2  # Golden apple gives 2 points
            else:
                score += 1  # Regular apple gives 1 point
            apple["is_gold"] = random.random() < 0.43  # 43% chance to spawn a golden apple
            apple["x"] = random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE
            apple["y"] = random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE

        # Check for collisions with itself
        for segment in snake["body"][1:]:
            if snake["x"] == segment[0] and snake["y"] == segment[1]:
                game_active = False  # End the game on collision

        # Draw the apple (or golden apple)
        if apple["is_gold"]:
            screen.blit(golden_apple_sprite, (apple["x"], apple["y"]))
        else:
            screen.blit(apple_sprite, (apple["x"], apple["y"]))

        # Draw the snake
        for segment in snake["body"]:
            pygame.draw.rect(screen, snake["color"], (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Display the score
        display_score()

        # Increase the FPS cap every 10 scores
        fps_cap = 12 + score // 10  # For every 10 scores, increase the FPS cap by 1

    # If the game is over, display the game over screen
    if not game_active:
        game_over()

    # Refresh the screen
    pygame.display.flip()

    # Cap the frame rate (it increases with score)
    clock.tick(fps_cap)

# Quit Pygame
pygame.quit()
