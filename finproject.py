import pygame
import math
import sys

pygame.init()

# screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incline Force Simulator")

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

    # update speed along incline based on acceleration
    speed_x += acceleration * math.cos(angle_rad) * 0.1
    speed_y += acceleration * math.sin(angle_rad) * 0.1

    return F_parallel, F_perpendicular


pygame.quit()
sys.exit()
