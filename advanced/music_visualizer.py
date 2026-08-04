import pygame
import numpy as np
import sounddevice as sd

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")
clock = pygame.time.Clock()

# Audio settings
SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

# Colors
BG_COLOR = (10, 10, 10)
BAR_COLOR = (0, 200, 255)

audio_data = np.zeros(BLOCK_SIZE)

def audio_callback(indata, frames, time, status):
    global audio_data
    audio_data = indata[:, 0]

stream = sd.InputStream(
    channels=1,
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    callback=audio_callback
)

stream.start()

running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # FFT (frequency analysis)
    fft_data = np.abs(np.fft.fft(audio_data))[:BLOCK_SIZE // 2]
    fft_data = fft_data / np.max(fft_data + 1e-6)

    bar_width = WIDTH // len(fft_data) * 6
    x = 0

    for value in fft_data[::6]:
        bar_height = int(value * HEIGHT)
        pygame.draw.rect(
            screen,
            BAR_COLOR,
            (x, HEIGHT - bar_height, bar_width, bar_height),
        )
        x += bar_width + 1

    pygame.display.flip()

stream.stop()
pygame.quit()

