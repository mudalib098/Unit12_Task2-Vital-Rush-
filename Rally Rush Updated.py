import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong Final")

# Colours
WHITE = (255, 255, 255)
BLUE = (80, 180, 255)
PINK = (255, 120, 180)
GREEN = (120, 255, 120)
BLACK = (0, 0, 0)

# Game settings
paddle_width, paddle_height = 10, 100
paddle_speed = 7
ball_size = 15

font = pygame.font.Font(None, 70)
small_font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()


def reset_ball(ball, direction):
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return 5 * direction, random.choice([-4, -3, 3, 4])


# TITLE SCREEN
def title_screen():
    while True:
        screen.fill(BLACK)

        title = font.render("PY PONG", True, WHITE)
        start = small_font.render("Press SPACE to Start", True, BLUE)
        info = small_font.render("2 Player + CPU Mode", True, PINK)

        screen.blit(title, (WIDTH//2 - 120, 150))
        screen.blit(start, (WIDTH//2 - 160, 300))
        screen.blit(info, (WIDTH//2 - 140, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return


# MENU SCREEN
def menu():
    while True:
        screen.fill(BLACK)

        title = font.render("SELECT MODE", True, WHITE)
        option1 = small_font.render("Press 1: 2 Player", True, BLUE)
        option2 = small_font.render("Press 2: vs CPU", True, PINK)

        screen.blit(title, (WIDTH//2 - 170, 150))
        screen.blit(option1, (WIDTH//2 - 160, 300))
        screen.blit(option2, (WIDTH//2 - 160, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return "2P"
        if keys[pygame.K_2]:
            return "CPU"


# GAME LOOP
def game(mode):
    player1 = pygame.Rect(20, HEIGHT//2 - 50, paddle_width, paddle_height)
    player2 = pygame.Rect(WIDTH - 30, HEIGHT//2 - 50, paddle_width, paddle_height)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_size, ball_size)

    score1 = 0
    score2 = 0

    ball_speed_x = 5
    ball_speed_y = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Player 1 (W/S)
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= paddle_speed
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += paddle_speed

        # Player 2 / CPU
        if mode == "2P":
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= paddle_speed
            if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
                player2.y += paddle_speed
        else:
            # CPU AI
            if player2.centery < ball.centery:
                player2.y += paddle_speed - 2
            if player2.centery > ball.centery:
                player2.y -= paddle_speed - 2

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Wall bounce
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Paddle collision
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            score2 += 1
            ball_speed_x, ball_speed_y = reset_ball(ball, 1)

        if ball.right >= WIDTH:
            score1 += 1
            ball_speed_x, ball_speed_y = reset_ball(ball, -1)

        # Background
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PINK, (WIDTH//2, 0, WIDTH//2, HEIGHT))

        # Draw game objects
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, GREEN, ball)

        # Score display
        score_text = font.render(f"{score1}   {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 40, 20))

        pygame.display.flip()
        clock.tick(60)


# RUN GAME
title_screen()
mode = menu()
game(mode)
