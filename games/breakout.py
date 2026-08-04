import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 80, 80)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 30, 100, 12)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12)
ball_speed = [random.choice([-4, 4]), -4]

# Bricks
bricks = []
for row in range(5):
    for col in range(10):
        bricks.append(pygame.Rect(col * 80 + 5, row * 30 + 40, 70, 20))

score = 0
font = pygame.font.SysFont(None, 30)

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 6
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 6

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1

    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1
            score += 10
            break

    if ball.bottom >= HEIGHT:
        running = False

    draw()

pygame.quit()
sys.exit()

