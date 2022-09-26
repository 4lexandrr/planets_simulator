import sys
import pygame
import math

pygame.init()

#  инициализируем окно
screen_width = 1000
screen_height = 800
boyut = (screen_width, screen_height)
screen_window = pygame.display.set_mode(boyut)
pygame.display.set_caption('Planets Simulator')

FONT = pygame.font.SysFont("comicsans", 16)


class Planet():
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + screen_width / 2
        y = self.y * self.SCALE + screen_height / 2

        if len(self.orbit) > 2:
            updating_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + screen_width / 2
                y = y * self.SCALE + screen_height / 2
                updating_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updating_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        # Compute the distance of the other body.
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        # Compute the force of attraction
        f = self.G * self.mass * other.mass / distance ** 2

        # Compute the direction of the force.
        theta = math.atan2(distance_y, distance_x)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

    def update_positions(self, planets):
        total_fx = 0
        total_fy = 0
        for element in planets:
            if self == element:
                continue

            fx, fy = self.attraction(element)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


if __name__ == '__main__':
    clock = pygame.time.Clock()

    # Create a planets
    sun = Planet(0, 0, 30, (249, 215, 28), 1.98892 * 10 ** 30)
    sun.sun = True

    mercury = Planet(0.3871 * Planet.AU, 0, 10, (202, 185, 186), 3.33022 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.7232 * Planet.AU, 0, 15, (246, 157, 97), 4.867 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 15, (87, 71, 30), 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.5236 * Planet.AU, 0, 30, (156, 46, 53), 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, earth, mercury, venus, mars]

    while True:
        clock.tick(60)  # 60 fps
        screen_window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for planet in planets:
            planet.update_positions(planets)
            planet.draw(screen_window)

        pygame.display.update()