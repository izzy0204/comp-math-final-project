import pygame
import math
import sys

pygame.init()

# screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incline Force Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

FONT = pygame.font.Font(None, 28)
LARGE_FONT = pygame.font.Font(None, 36)

# gravity constant in (m/s²)
g = 9.8

# simulation state
paused = False

# incline and object properties
class Simulator:
    def __init__(self):
        self.mass = 10.0  # mass (kg)
        self.angle = 30  # incline angle (degrees)
        self.friction = 0.2  # coefficient of friction
        self.reset_simulation()

    def reset_simulation(self):
        self.velocity = 0  # initial velocity
        # start from the top-right of the incline
        self.position_x = WIDTH - 100  # starting x-position
        self.position_y = 100  # starting y-position
        self.time_step = 1 / 60  # simulation time step

    def calculate_forces(self):
        angle_rad = math.radians(self.angle)
        weight = self.mass * g
        normal_force = weight * math.cos(angle_rad)
        parallel_force = weight * math.sin(angle_rad)
        friction_force = self.friction * normal_force

        net_force = parallel_force - friction_force
        acceleration = net_force / self.mass

        if net_force < 0:
            acceleration = 0  # Object doesn't move down the incline

        return normal_force, friction_force, parallel_force, acceleration

    def update_position(self):
        _, _, _, acceleration = self.calculate_forces()
        self.velocity += acceleration * self.time_step
        displacement = self.velocity * self.time_step

        # update position along incline
        angle_rad = math.radians(self.angle)
        # move left (decrease x) and down (increase y) along the incline
        self.position_x -= displacement * math.cos(angle_rad)
        self.position_y += displacement * math.sin(angle_rad)

        # stop if object reaches the bottom
        if self.position_x <= 200:
            self.velocity = 0

simulator = Simulator()

buttons = {
    "mass_up": pygame.Rect(50, 100, 40, 40),
    "mass_down": pygame.Rect(100, 100, 40, 40),
    "angle_up": pygame.Rect(50, 160, 40, 40),
    "angle_down": pygame.Rect(100, 160, 40, 40),
    "friction_up": pygame.Rect(50, 220, 40, 40),
    "friction_down": pygame.Rect(100, 220, 40, 40),
    "reset": pygame.Rect(WIDTH - 140, 50, 100, 40),
    "pause": pygame.Rect(WIDTH - 140, 110, 100, 40),
}

# draw text
def draw_text(text, x, y, font=FONT, color=BLACK):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# draw buttons
def draw_buttons():
    pygame.draw.rect(screen, GRAY, buttons["mass_up"])
    pygame.draw.rect(screen, GRAY, buttons["mass_down"])
    pygame.draw.rect(screen, GRAY, buttons["angle_up"])
    pygame.draw.rect(screen, GRAY, buttons["angle_down"])
    pygame.draw.rect(screen, GRAY, buttons["friction_up"])
    pygame.draw.rect(screen, GRAY, buttons["friction_down"])
    pygame.draw.rect(screen, GRAY, buttons["reset"])
    pygame.draw.rect(screen, GRAY, buttons["pause"])

    draw_text("+", 62, 110)
    draw_text("-", 112, 110)
    draw_text("+", 62, 170)
    draw_text("-", 112, 170)
    draw_text("+", 62, 230)
    draw_text("-", 112, 230)
    draw_text("Reset", WIDTH - 125, 60, LARGE_FONT)
    draw_text("Pause" if not paused else "Play", WIDTH - 125, 120, LARGE_FONT)

# main loop
def main():
    global paused
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # draw incline
        incline_start = (WIDTH - 100, 100)
        incline_end = (200, HEIGHT - 100)
        pygame.draw.line(screen, BLACK, incline_start, incline_end, 3)

        # draw object
        pygame.draw.rect(screen, RED, (simulator.position_x - 10, simulator.position_y - 10, 20, 20))

        # forces visualization
        normal_force, friction_force, parallel_force, _ = simulator.calculate_forces()
        angle_rad = math.radians(simulator.angle)

        # draw force vectors
        pygame.draw.line(screen, BLUE, (simulator.position_x, simulator.position_y),
                         (simulator.position_x, simulator.position_y + normal_force * 0.5), 2)
        pygame.draw.line(screen, GREEN, (simulator.position_x, simulator.position_y),
                         (simulator.position_x - parallel_force * 0.5, simulator.position_y), 2)

        # draw force labels
        draw_text(f"Normal: {normal_force:.2f} N", 10, HEIGHT - 180)
        draw_text(f"Friction: {friction_force:.2f} N", 10, HEIGHT - 150)
        draw_text(f"Parallel: {parallel_force:.2f} N", 10, HEIGHT - 120)

        # update simulation
        if not paused:
            simulator.update_position()

        # draw buttons and values
        draw_buttons()
        draw_text(f"Mass: {simulator.mass} kg", 10, 20)
        draw_text(f"Angle: {simulator.angle}°", 10, 50)
        draw_text(f"Friction: {simulator.friction:.2f}", 10, 80)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["mass_up"].collidepoint(event.pos):
                    simulator.mass += 1
                elif buttons["mass_down"].collidepoint(event.pos) and simulator.mass > 1:
                    simulator.mass -= 1
                elif buttons["angle_up"].collidepoint(event.pos) and simulator.angle < 85:
                    simulator.angle += 1
                elif buttons["angle_down"].collidepoint(event.pos) and simulator.angle > 0:
                    simulator.angle -= 1
                elif buttons["friction_up"].collidepoint(event.pos) and simulator.friction < 1:
                    simulator.friction += 0.05
                elif buttons["friction_down"].collidepoint(event.pos) and simulator.friction > 0:
                    simulator.friction -= 0.05
                elif buttons["reset"].collidepoint(event.pos):
                    simulator.reset_simulation()
                elif buttons["pause"].collidepoint(event.pos):
                    paused = not paused

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
