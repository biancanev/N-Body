from bodies import *
import pygame

#Constants for simulation
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
km_per_pixel = 200
m_per_pixel = km_per_pixel * 1000
mass_stability_scale = 1e-15
distance_stability_scale = 10
G = 6.67 * (10 ** -11) #expressed in m^3/(kg*s^2)
G_SCALED = G * (m_per_pixel ** 3) * mass_stability_scale
dt = 10 #expressed in seconds

#Nice real-life bodies to simulate
E_TO_M = 384400 #in km
EARTH = Body(400, 300, 5.972 * (10**24) * mass_stability_scale, 0, 0, BLUE, round(6357/km_per_pixel))
MOON = Body(400, 300 + round(E_TO_M / km_per_pixel) / distance_stability_scale, 7.348 * (10**22) * mass_stability_scale, 1.022 / distance_stability_scale, 0, WHITE, round(1738/km_per_pixel))
MOON2 = Body(400, 300 - round(E_TO_M / km_per_pixel) / distance_stability_scale, 7.348 * (10**22) * mass_stability_scale, 1.022 / distance_stability_scale, 0, WHITE, round(1738/km_per_pixel))

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('N-Body Simulation')

"""
Coordinate system definition:
X: + is right, - is left
Y: + is down, - is up
origin is the top left corner
"""

bodies = [EARTH, MOON]

#for verlet
for body in bodies:
    body.prev = body.position - body.velocity * dt

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    calculate(bodies, G_SCALED)
    update(bodies, dt)

    screen.fill(BLACK)


    for body in bodies:
        #nice tracer graphics
        body.tracer.append((int(body.position[0]), int(body.position[1])))
        if len(body.tracer) > 1500:
            body.tracer.pop(0)


        x, y = body.position.flatten()
        x, y = int(x), int(y)
        pygame.draw.circle(screen, body.color, (x, y), body.radius)
        if len(body.tracer) > 1:
            pygame.draw.lines(screen, body.color, False, body.tracer, 2)

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
