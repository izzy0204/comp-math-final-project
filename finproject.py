import pygame
import math
import sys

pygame.init()

# screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incline Force Simulator")

# grid setup
GRID_SIZE = 32
GRID_COLS = 20
GRID_ROWS = 16

# colors


# convert angle to radians
angle_rad = math.radians(angle)

# initial position and speed of the object
x, y = 200, 300
speed_x, speed_y = 0, 0


# calculate forces
def calculate_forces():
    global speed_x, speed_y

    Fg = mass * g

    F_parallel = Fg * math.sin(angle_rad)
    F_perpendicular = Fg * math.cos(angle_rad)

    F_friction = friction_coefficient * F_perpendicular

    F_net = F_parallel - F_friction

    acceleration = F_net / mass

    # speed along incline based on acceleration
    speed_x += acceleration * math.cos(angle_rad)
    speed_y += acceleration * math.sin(angle_rad)

    return F_parallel, F_perpendicular


pygame.quit()
sys.exit()
