import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incline Force Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

FONT = pygame.font.Font('monofonto rg.otf', 18) # Open source free font from dafont.com
LARGE_FONT = pygame.font.Font('monofonto rg.otf', 28)

# Gravity constant (m/s²)
g = 9.8

# Simulation state
paused = False


class Simulator:
    """
    A class to simulate the motion of an object on an inclined plane considering gravity,
    friction, and other forces.

    Attributes:
        mass (float): The mass of the object (in kg).
        angle (float): The angle of the incline (in degrees).
        friction (float): The coefficient of friction between the object and the incline.
        incline_start (tuple): The starting point of the incline on the screen (x, y).
        incline_end (tuple): The end point of the incline on the screen (x, y).
        progress (float): The progress of the object on the incline, ranging from 0.0 (top) to 1.0 (bottom).
        velocity (float): The velocity of the object.
        position_x (float): The current x-coordinate of the object on the incline.
        position_y (float): The current y-coordinate of the object on the incline.
        incline_length (float): The length of the incline.
        slope_x (float): The horizontal distance between the start and end points of the incline.
        slope_y (float): The vertical distance between the start and end points of the incline.
    """
    def __init__(self):
        """
        Initializes the simulator with default properties (mass, angle, friction) and sets up
        the parameters of the incline and object position.
        """
        self.mass = 10.0
        self.angle = 30
        self.friction = 0.2

        self.incline_start = (WIDTH - 100, 100)
        self.incline_end = (200, HEIGHT - 100)

        self.progress = 0.0

        self.slope_x = self.incline_end[0] - self.incline_start[0]
        self.slope_y = self.incline_end[1] - self.incline_start[1]
        self.incline_length = math.sqrt(self.slope_x ** 2 + self.slope_y ** 2)

        self.reset_simulation()

    def reset_simulation(self):
        """
        Resets the simulation, setting the object back to the top of the incline with an initial 
        velocity of zero.
        """
        self.velocity = 0
        self.progress = 0.0
        self.position_x = self.incline_start[0]
        self.position_y = self.incline_start[1]

    def calculate_forces(self):
        """
        Calculates the forces acting on the object: normal force, parallel force, frictional force,
        and the net acceleration.

        Returns:
            tuple: A tuple containing the normal force, friction force, parallel force, and acceleration.
        """
        angle_rad = math.radians(self.angle)
        weight = self.mass * g

        normal_force = weight * math.cos(angle_rad)
        parallel_force = weight * math.sin(angle_rad)
        friction_force = self.friction * normal_force

        net_force = parallel_force - friction_force
        acceleration = net_force / self.mass if net_force > 0 else 0

        return normal_force, friction_force, parallel_force, acceleration

    def update_position(self):
        """
        Updates the object's position on the incline based on its velocity and acceleration.

        If the object reaches the bottom of the incline (progress >= 1.0), it stops moving.
        """
        if self.progress >= 1.0:
            self.velocity = 0
            return

        _, _, _, acceleration = self.calculate_forces()
        self.velocity += acceleration * (1 / 60)
        displacement = self.velocity * (1 / 60)

        progress_increment = displacement / self.incline_length
        self.progress = min(self.progress + progress_increment, 1.0)

        self.position_x = self.incline_start[0] + self.slope_x * self.progress
        self.position_y = self.incline_start[1] + self.slope_y * self.progress

def draw_grid():
    """
    Draws a grid overlay on the screen to aid visualization of the simulation.
    
    The grid is spaced at 20 pixels intervals and is rendered in a light gray color.
    """
    spacing = 20 
    for x in range(0, WIDTH, spacing):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, spacing):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)

def draw_text(text, x, y, font=FONT, color=BLACK):
    """
    Renders text on the screen at the specified coordinates.

    Args:
        text (str): The text to display.
        x (int): X-coordinate for the text position.
        y (int): Y-coordinate for the text position.
        font (pygame.font.Font): The font to use for rendering the text.
        color (tuple): RGB color tuple for the text.
    """
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_buttons():
    """
    Draws interactive buttons on the screen for controlling the simulation.

    The buttons include options to adjust mass, angle, friction, reset the simulation,
    and toggle the pause state. Labels are displayed alongside the buttons.
    """
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

def draw_arrow(start, end, color, width=2):
    """
    Draws an arrow on the screen between two points.

    Args:
        start (tuple): Coordinates of the arrow's starting point (x, y).
        end (tuple): Coordinates of the arrow's end point (x, y).
        color (tuple): RGB color tuple for the arrow.
        width (int): Line width for the arrow shaft.
    """
    pygame.draw.line(screen, color, start, end, width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_size = 8
    arrow_angle = math.pi / 6
    points = [
        end,
        (end[0] - arrow_size * math.cos(angle - arrow_angle),
         end[1] - arrow_size * math.sin(angle - arrow_angle)),
        (end[0] - arrow_size * math.cos(angle + arrow_angle),
         end[1] - arrow_size * math.sin(angle + arrow_angle))
    ]
    pygame.draw.polygon(screen, color, points)


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

def draw_angle_display(simulator):
    """
    Displays the incline angle near the lower end of the slope.

    Args:
        simulator (Simulator): The current simulator instance containing the angle value.
    """
    angle_x = simulator.incline_end[0] + 40
    angle_y = simulator.incline_end[1] - 30
    draw_text(f"{simulator.angle}°", angle_x, angle_y, FONT, BLACK)

def main():
    global paused
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid()
        pygame.draw.line(screen, GRAY, simulator.incline_start, simulator.incline_end, 5)
        lowest_point = simulator.incline_end
        pygame.draw.line(screen, BLACK, lowest_point, (lowest_point[0] + 500, lowest_point[1]), 2)

        pygame.draw.rect(
            screen,
            RED,
            pygame.Rect(
                int(simulator.position_x) - 10,
                int(simulator.position_y) - 10,
                20,
                20
            )
        )

        normal_force, friction_force, parallel_force, acceleration = simulator.calculate_forces()
        scale = simulator.incline_length / 100

        draw_arrow((simulator.position_x, simulator.position_y),
                   (simulator.position_x, simulator.position_y + normal_force * scale), BLUE)
        draw_arrow((simulator.position_x, simulator.position_y),
                   (simulator.position_x - parallel_force * scale, simulator.position_y), GREEN)

        draw_text(f"Normal: {normal_force:.2f} N", 10, HEIGHT - 200)
        draw_text(f"Friction: {friction_force:.2f} N", 10, HEIGHT - 170)
        draw_text(f"Parallel: {parallel_force:.2f} N", 10, HEIGHT - 140)

        draw_text(f"Speed: {simulator.velocity:.2f} m/s", 10, HEIGHT - 110)
        draw_text(f"Acceleration: {acceleration:.2f} m/s²", 10, HEIGHT - 80)

        draw_angle_display(simulator)

        if not paused:
            simulator.update_position()

        draw_buttons()
        draw_text(f"Mass: {simulator.mass} kg", 10, 20)
        draw_text(f"Angle: {simulator.angle}°", 10, 50)
        draw_text(f"Friction: {simulator.friction:.2f}", 10, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["mass_up"].collidepoint(event.pos):
                    simulator.mass = min(simulator.mass + 1, 100)
                elif buttons["mass_down"].collidepoint(event.pos):
                    simulator.mass = max(1, simulator.mass - 1)
                elif buttons["angle_up"].collidepoint(event.pos):
                    simulator.angle = min(85, simulator.angle + 1)
                elif buttons["angle_down"].collidepoint(event.pos):
                    simulator.angle = max(0, simulator.angle - 1)
                elif buttons["friction_up"].collidepoint(event.pos):
                    simulator.friction = min(1.0, round(simulator.friction + 0.05, 2))
                elif buttons["friction_down"].collidepoint(event.pos):
                    simulator.friction = max(0, round(simulator.friction - 0.05, 2))
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
