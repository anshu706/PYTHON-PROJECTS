import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Object Viewer")

gluPerspective(45, WIDTH / HEIGHT, 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

rotation_x, rotation_y = 0, 0
zoom = -5
dragging = False
last_pos = None

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 7), (3, 6)
)


def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3f(1, 1, 1)
            glVertex3fv(vertices[vertex])
    glEnd()


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                last_pos = event.pos
            if event.button == 4:
                zoom += 0.3
            if event.button == 5:
                zoom -= 0.3

        if event.type == MOUSEBUTTONUP:
            dragging = False

        if event.type == MOUSEMOTION and dragging:
            dx, dy = event.rel
            rotation_x += dy
            rotation_y += dx

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    glTranslatef(0, 0, zoom)
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)
    glScalef(0.1, 0.1, 0.1)

    draw_cube()
    pygame.display.flip()

pygame.quit()
