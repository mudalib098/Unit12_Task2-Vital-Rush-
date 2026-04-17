import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")

# Colours
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
PINK = (255, 100, 150)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)

# Paddle settings
paddle_width, paddle_height = 10, 100
paddle_speed = 6

# Ball settings
ball_size = 15
ball_speed_x = 5
ball_speed_y = 5

# Create paddles and ball
player1 = pygame.Rect(20, HEIGHT//2 - 50, paddle_width, paddle_height)
player2 = pygame.Rect(WIDTH - 30, HEIGHT//2 - 50, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_size, ball_size)

# Score
score1 = 0
score2 = 0
font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key inputs
    keys = pygame.key.get_pressed()

    # Player 1 (W/S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed

    # Player 2 (UP/DOWN)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle collision
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        score2 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if ball.right >= WIDTH:
        score1 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    # Draw colourful background
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH//2, HEIGHT))
    pygame.draw.rect(screen, PINK, (WIDTH//2, 0, WIDTH//2, HEIGHT))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, GREEN, ball)

    # Draw scores
    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)

    screen.blit(score_text1, (WIDTH//4, 20))
    screen.blit(score_text2, (WIDTH*3//4, 20))

    pygame.display.flip()
    clock.tick(60)
