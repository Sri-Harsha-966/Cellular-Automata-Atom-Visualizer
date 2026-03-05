import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import csv
from OpenGL.GLU import gluPerspective


# Load electron cloud data from CSV (including orbitals and colors)
particles = []
orbital_groups = {}

with open("electron_cloud.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        x, y, z, r, g, b, orbital_id = map(float, row)
        orbital_id = int(orbital_id)  # Convert to integer
        color = (r / 255, g / 255, b / 255)
        point = (x, y, z, *color)

        particles.append(point)  # Store all points

        if orbital_id not in orbital_groups:
            orbital_groups[orbital_id] = []
        orbital_groups[orbital_id].append(point)

# Track which orbitals are visible
visible_orbitals = {orbital_id: True for orbital_id in orbital_groups}  # All orbitals visible by default


# Pygame and OpenGL initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
glEnable(GL_POINT_SMOOTH)  # Smooth particles
glPointSize(2)  # Adjust particle size
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_DEPTH_TEST)  # Enable 3D depth

# Set perspective
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Move camera back
glTranslatef(0, 0, -5)

# Main loop
running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif K_0 <= event.key <= K_9:  # Toggle orbitals 0-9
                orbital_index = event.key - K_0  # Convert key press to number
                if orbital_index == 0:
                    # Toggle all orbitals
                    all_visible = any(visible_orbitals.values())
                    for key in visible_orbitals:
                        visible_orbitals[key] = not all_visible
                else:
                    # Toggle specific orbital
                    if orbital_index - 1 in visible_orbitals:
                        visible_orbitals[orbital_index - 1] = not visible_orbitals[orbital_index - 1]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen
    glLoadIdentity()
    glTranslatef(0, 0, -5)

    # Rotate the cloud for visualization
    glRotatef(angle, 0, 1, 0)
    angle += 0.5  # Adjust rotation speed

    # Draw electron cloud with colors
    glBegin(GL_POINTS)
    for orbital_id, points in orbital_groups.items():
        if visible_orbitals[orbital_id]:  # Only render visible orbitals
            for x, y, z, r, g, b in points:
                glColor3f(r, g, b)  # Set color dynamically
                glVertex3f(x, y, z)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)  # Control frame rate

pygame.quit()
