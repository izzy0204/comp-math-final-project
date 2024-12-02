import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incline Force Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
FONT = pygame.font.Font(None, 24)
LARGE_FONT = pygame.font.Font(None, 36)

# Physics constants
g = 9.8  # Gravity (m/s²)

# Simulation state
paused = False

# Incline and object properties
class Simulator:
    def __init__(self):
        self.mass = 10.0  # Mass (kg)
        self.angle = 30  # Incline angle (degrees)
        self.friction = 0.2  # Coefficient of friction
        self.reset_simulation()

    def reset_simulation(self):
        self.velocity = 0  # Initial velocity
        # Start from the top-right of the incline
        self.position_x = WIDTH - 100  # Starting x-position
        self.position_y = 100  # Starting y-position
        self.time_step = 1 / 60  # Simulation time step

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

        # Update position along incline
        angle_rad = math.radians(self.angle)
        # Move left (decrease x) and down (increase y) along the incline
        self.position_x -= displacement * math.cos(angle_rad)
        self.position_y += displacement * math.sin(angle_rad)

        # Stop if object reaches the bottom
        if self.position_x <= 200:
            self.velocity = 0

# Simulator instance
simulator = Simulator()

# Buttons
buttons = {
    "mass_up": pygame.Rect(50, 50, 40, 40),
    "mass_down": pygame.Rect(100, 50, 40, 40),
    "angle_up": pygame.Rect(50, 100, 40, 40),
    "angle_down": pygame.Rect(100, 100, 40, 40),
    "friction_up": pygame.Rect(50, 150, 40, 40),
    "friction_down": pygame.Rect(100, 150, 40, 40),
    "reset": pygame.Rect(WIDTH - 150, 50, 100, 40),
    "pause": pygame.Rect(WIDTH - 150, 100, 100, 40),
}

# Draw text
def draw_text(text, x, y, font=FONT, color=BLACK):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Draw buttons
def draw_buttons():
    pygame.draw.rect(screen, GRAY, buttons["mass_up"])
    pygame.draw.rect(screen, GRAY, buttons["mass_down"])
    pygame.draw.rect(screen, GRAY, buttons["angle_up"])
    pygame.draw.rect(screen, GRAY, buttons["angle_down"])
    pygame.draw.rect(screen, GRAY, buttons["friction_up"])
    pygame.draw.rect(screen, GRAY, buttons["friction_down"])
    pygame.draw.rect(screen, GRAY, buttons["reset"])
    pygame.draw.rect(screen, GRAY, buttons["pause"])

    draw_text("+", 60, 55)
    draw_text("-", 110, 55)
    draw_text("+", 60, 105)
    draw_text("-", 110, 105)
    draw_text("+", 60, 155)
    draw_text("-", 110, 155)
    draw_text("Reset", WIDTH - 140, 60)
    draw_text("Pause" if not paused else "Play", WIDTH - 140, 110)

# Main loop
def main():
    global paused
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw incline
        incline_start = (WIDTH - 100, 100)
        incline_end = (200, HEIGHT - 100)
        pygame.draw.line(screen, BLACK, incline_start, incline_end, 3)

        # Draw object
        pygame.draw.rect(screen, RED, (simulator.position_x - 10, simulator.position_y - 10, 20, 20))

        # Forces visualization
        normal_force, friction_force, parallel_force, _ = simulator.calculate_forces()
        angle_rad = math.radians(simulator.angle)

        # Draw force vectors
        pygame.draw.line(screen, BLUE, (simulator.position_x, simulator.position_y),
                         (simulator.position_x, simulator.position_y + normal_force * 0.5), 2)
        pygame.draw.line(screen, GREEN, (simulator.position_x, simulator.position_y),
                         (simulator.position_x - parallel_force * 0.5, simulator.position_y), 2)

        # Draw force labels
        draw_text(f"Normal: {normal_force:.2f} N", 10, HEIGHT - 150)
        draw_text(f"Friction: {friction_force:.2f} N", 10, HEIGHT - 130)
        draw_text(f"Parallel: {parallel_force:.2f} N", 10, HEIGHT - 110)

        # Update simulation
        if not paused:
            simulator.update_position()

        # Draw buttons and values
        draw_buttons()
        draw_text(f"Mass: {simulator.mass} kg", 10, 10)
        draw_text(f"Angle: {simulator.angle}°", 10, 30)
        draw_text(f"Friction: {simulator.friction}", 10, 50)

        # Handle events
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