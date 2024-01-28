import pygame
import random
import math

# Initialize Pygame
pygame.init()
width, height = 800, 800  # Set the dimensions of the game window
screen = pygame.display.set_mode((width, height))  # Create the game window
pygame.display.set_caption('Pong Wars')  # Set the window title

# Define vivid pink color for the score text
VIVID_PINK = (255, 105, 180)  # RGB values for bright pink

# Define colors and constants
DAY_COLOR = (217, 232, 227)  # Light mint color
NIGHT_COLOR = (23, 43, 54)   # Dark navy color
DAY_BALL_COLOR = NIGHT_COLOR  # Ball color for day
NIGHT_BALL_COLOR = DAY_COLOR  # Ball color for night
SQUARE_SIZE = 25  # Size of each square in the grid

# Initialize font for score display
pygame.font.init()
score_font = pygame.font.SysFont("monospace", 20)  # Font for the score text

# Ball properties
x1, y1 = width / 4, height / 2  # Initial position of the first ball
dx1, dy1 = 14, 14  # Velocity of the first ball
x2, y2 = (width / 4) * 3, height / 2  # Initial position of the second ball
dx2, dy2 = -14, -14  # Velocity of the second ball

# Initialize squares for the background
numSquaresX, numSquaresY = width // SQUARE_SIZE, height // SQUARE_SIZE
squares = [[DAY_COLOR if i < numSquaresX // 2 else NIGHT_COLOR for j in range(numSquaresY)] for i in range(numSquaresX)]

# Function to draw a ball
def drawBall(screen, x, y, color):
    pygame.draw.circle(screen, color, (int(x), int(y)), SQUARE_SIZE // 2)

# Function to draw squares for the background
def drawSquares(screen, squares):
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            pygame.draw.rect(screen, squares[i][j],
                             (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to generate a random number within a range
def randomNum(min, max):
    return random.uniform(min, max)

# Function to update the square color on collision and bounce the ball
def updateSquareAndBounce(x, y, dx, dy, color, squares):
    updatedDx, updatedDy = dx, dy
    for angle in range(0, 360, 45):
        checkX = x + math.cos(math.radians(angle)) * (SQUARE_SIZE / 2)
        checkY = y + math.sin(math.radians(angle)) * (SQUARE_SIZE / 2)
        i, j = int(checkX // SQUARE_SIZE), int(checkY // SQUARE_SIZE)
        if 0 <= i < len(squares) and 0 <= j < len(squares[0]):
            if squares[i][j] != color:
                squares[i][j] = color
                if abs(math.cos(math.radians(angle))) > abs(math.sin(math.radians(angle))):
                    updatedDx = -updatedDx
                else:
                    updatedDy = -updatedDy
                updatedDx += randomNum(-0.01, 0.01)
                updatedDy += randomNum(-0.01, 0.01)
    return updatedDx, updatedDy

# Function to check and handle boundary collision
def checkBoundaryCollision(x, y, dx, dy, width, height):
    if x + dx > width - SQUARE_SIZE / 2 or x + dx < SQUARE_SIZE / 2:
        dx = -dx
    if y + dy > height - SQUARE_SIZE / 2 or y + dy < SQUARE_SIZE / 2:
        dy = -dy
    return dx, dy

# Function to update and display the score
def updateScoreElement(screen, squares, score_font):
    dayScore, nightScore = 0, 0
    for row in squares:
        for color in row:
            if color == DAY_COLOR:
                dayScore += 1
            elif color == NIGHT_COLOR:
                nightScore += 1
    score_text = f"Day: {dayScore} | Night: {nightScore}"
    score_surface = score_font.render(score_text, True, VIVID_PINK)  # Render score text in vivid pink
    screen.blit(score_surface, (20, 20))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Stop the game if the window is closed

    screen.fill((0, 0, 0))  # Clear the screen

    # Draw game elements
    drawSquares(screen, squares)
    drawBall(screen, x1, y1, DAY_BALL_COLOR)
    drawBall(screen, x2, y2, NIGHT_BALL_COLOR)

    # Update game state
    dx1, dy1 = updateSquareAndBounce(x1, y1, dx1, dy1, DAY_COLOR, squares)
    dx2, dy2 = updateSquareAndBounce(x2, y2, dx2, dy2, NIGHT_COLOR, squares)
    dx1, dy1 = checkBoundaryCollision(x1, y1, dx1, dy1, width, height)
    dx2, dy2 = checkBoundaryCollision(x2, y2, dx2, dy2, width, height)
    x1 += dx1
    y1 += dy1
    x2 += dx2
    y2 += dy2

    updateScoreElement(screen, squares, score_font)  # Update and display the score

    pygame.display.flip()  # Update the full display Surface to the screen
    pygame.time.Clock().tick(60)  # Cap the frame rate at 60 frames per second

pygame.quit()  # Quit Pygame when the game loop ends

