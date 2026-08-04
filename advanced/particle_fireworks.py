import pygame
import random
import math

import sys
import warnings

# Suppress the pkg_resources deprecation warning from pygame
warnings.filterwarnings("ignore", category=UserWarning,
                        module="pygame.pkgdata")

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Fireworks")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)

# Particle class


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(40, 80)
        self.color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255),
        )
        self.radius = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # gravity
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color,
                               (int(self.x), int(self.y)), self.radius)


particles = []

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Create fireworks on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for _ in range(120):
                particles.append(Particle(mx, my))

    # Update particles
    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0:
            particles.remove(p)

    pygame.display.flip()

pygame.quit()
