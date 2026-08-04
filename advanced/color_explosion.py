import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Explosion Gradient")
clock = pygame.time.Clock()

speed = 0.02
time = 0

def color(x, y, t):
    r = int(128 + 127 * math.sin(x * 0.01 + t))
    g = int(128 + 127 * math.sin(y * 0.01 + t + 2))
    b = int(128 + 127 * math.sin((x + y) * 0.01 + t + 4))
    return r, g, b

running = True
while running:
    clock.tick(60)
    time += speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed += 0.01
            if event.key == pygame.K_DOWN:
                speed = max(0.01, speed - 0.01)

    for x in range(0, WIDTH, 4):
        for y in range(0, HEIGHT, 4):
            pygame.draw.rect(
                screen,
                color(x, y, time),
                (x, y, 4, 4)
            )

    pygame.display.flip()

pygame.quit()

