import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Morph Animation")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 80, bold=True)

WORDS = ["PYTHON", "ANIMATION", "CREATIVE", "POWERFUL", "AWESOME"]
word_index = 0

alpha = 0
scale = 0.5
fade_in = True

def draw_text(text, alpha, scale):
    text_surface = FONT.render(text, True, (255, 255, 255))
    text_surface.set_alpha(alpha)

    size = text_surface.get_size()
    scaled = pygame.transform.smoothscale(
        text_surface,
        (int(size[0] * scale), int(size[1] * scale))
    )

    rect = scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(scaled, rect)

running = True
while running:
    clock.tick(60)
    screen.fill((20, 20, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if fade_in:
        alpha += 6
        scale += 0.01
        if alpha >= 255:
            fade_in = False
    else:
        alpha -= 6
        scale -= 0.01
        if alpha <= 0:
            fade_in = True
            scale = 0.5
            word_index = (word_index + 1) % len(WORDS)

    draw_text(WORDS[word_index], alpha, scale)

    pygame.display.flip()

pygame.quit()
sys.exit()

