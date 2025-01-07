import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from bodies import *
from gui import *
import argparse

#Handle any arguments passed to the python script
parser = argparse.ArgumentParser()
parser.add_argument(f"-v", "--verbosity", help="Debugger verbosity[LOW/MED/HIGH]")
parser.add_argument("-w", "--width", help="Screen width")
parser.add_argument("--height", help="Screen height")
args=parser.parse_args()

#Nice real-life bodies to simulate(default)
E_TO_M = 384400 #in km
EARTH = Body(400, 300, 5.972 * (10**24) * mass_stability_scale, 0, 0, BLUE, round(6357/km_per_pixel))
MOON = Body(400, 300 + round(E_TO_M / km_per_pixel) / distance_stability_scale, 7.348 * (10**22) * mass_stability_scale, 1.022 / distance_stability_scale, 0, WHITE, round(1738/km_per_pixel))
MOON2 = Body(400, 300 - round(E_TO_M / km_per_pixel) / distance_stability_scale, 7.348 * (10**23) * mass_stability_scale, 1.522 / distance_stability_scale, 0, BROWN, round(4738/km_per_pixel))

#GUI Screen Settigns
width, height = 1600, 1200
screen = pygame.display.set_mode((width, height), vsync=True)
pygame.display.set_caption('N-Body Simulation')

"""
Coordinate system definition:
X: + is right, - is left
Y: + is down, - is up
origin is the top left corner
"""

#set up bodies for simulation
bodies = config["bodies"] if "bodies" in config and config["bodies"] else [EARTH, MOON, MOON2]

#Store default values for when the simulation is reset
default_pos = [body.position.copy() for body in bodies]
default_vel = [body.velocity.copy() for body in bodies]
default_prev = [body.position.copy() - body.velocity * dt for body in bodies]
default_bodies = bodies[:]

#Set up previous vector for Verlet integration
for body in bodies:
    body.prev = body.position - body.velocity * dt
    

# Function to draw a slider
def draw_slider(label, value, x, y, min_val, max_val, step):
    pygame.draw.rect(screen, SLIDER_BG_COLOR, (x, y, 150, 10))  # Slider background
    pygame.draw.rect(screen, SLIDER_COLOR, (x + (value - min_val) / (max_val - min_val) * 150 - 5, y - 5, 10, 20))  # Slider handle
    
    # Draw label
    label_text = font.render(f"{label}: {value:.2e}", True, BLACK)
    screen.blit(label_text, (x + 160, y - 10))

# Function to draw a button
def draw_button(label, x, y, width, height):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))  # Button background
    button_text = font.render(label, True, WHITE)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

#Simulation variables to control pausing and exiting
running = True
is_running = False

#clock for animation
clock = pygame.time.Clock()

#simulation gui objects
g_slider = Slider("G", G, 40, 60, 0, 1e-9, 1e-11, screen)
dt_slider = Slider("dt", dt, 40, 120, 1, 10, 0.010, screen)
start_stop_button = Button("Start/Stop", 50, 180, 100, 40, screen)
reset_button = Button("Reset", 50, 240, 100, 40, screen)

#TODO: draw a frame when resetting or when first loading
def draw_frame():
    draw_sidebar(screen, height)
    g_slider.draw()
    dt_slider.draw()
    start_stop_button.draw()
    reset_button.draw()
    for i, body in enumerate(bodies):
        x, y = body.position.flatten()
        x, y = int(x), int(y)
        #Draw body
        pygame.draw.circle(screen, body.color, (x, y), body.radius)
    pygame.display.flip()

#pause function
def pause():
    global is_running
    is_running = not is_running
    print(f"DEBUG: Paused, G={G}, dt={dt}")

#reset function
def reset():
    bodies = default_bodies[:]
    #set all attributes back to stored defaults
    for i in range(len(bodies)):
        bodies[i].position = default_pos[i].copy()
        bodies[i].velocity = default_vel[i].copy()
        bodies[i].prev = default_prev[i].copy()
        bodies[i].acceleration = np.zeros_like(bodies[i].acceleration)
        bodies[i].tracer = []
        print(f"DEBUG: Reset, G={G}, dt={dt}")
    #TODO: figure out why this does not work as inteneded
    if not is_running:
        draw_frame()

#Begin the simulation
print(f"DEBUG: Simulation started, G={G}, dt={dt}, km-per-pixel={km_per_pixel}, distance-scaling={distance_stability_scale}, mass-scaling={mass_stability_scale}")
draw_frame()
while running:
    #Get user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        g_slider.update(event)
        dt_slider.update(event)
        start_stop_button.check_click(event, pause)
        reset_button.check_click(event, reset)
    
    #Check for paused state
    if not is_running:
        continue
    
    #GUI inputs
    G = g_slider.value
    dt = dt_slider.value

    #simulate
    calculate(bodies, G_SCALED)
    update(bodies, dt)

    screen.fill(BLACK)

    #Draw GUI elemnets
    draw_sidebar(screen, height)
    g_slider.draw()
    dt_slider.draw()
    start_stop_button.draw()
    reset_button.draw()

    #nice graphics
    for i, body in enumerate(bodies):

        #collision detection
        for j in range(i+1, len(bodies)):
            handle_colision(bodies[i], bodies[j], bodies, G_SCALED, dt)

        #nice tracer graphics
        body.tracer.append((int(body.position[0]), int(body.position[1])))
        if len(body.tracer) > 1500:
            body.tracer.pop(0)

        x, y = body.position.flatten()
        x, y = int(x), int(y)
        #Draw body
        pygame.draw.circle(screen, body.color, (x, y), body.radius)
        #draw tracers
        if TRACER and len(body.tracer) > 1:
            pygame.draw.lines(screen, body.color, False, body.tracer, 2)
        #draw vectors
        origin = (int(body.position[0]), int(body.position[1]))
        draw_vector(screen, origin, body.velocity.flatten(), RED, 1000)
        draw_vector(screen, origin, body.acceleration.flatten(), GREEN, 1e6)

        #draw key
        draw_vector(screen, (width - 160, 10), np.array([[30.0], [0.0]]).flatten(), RED)
        vel_label = font.render("Velocity", True, RED)
        screen.blit(vel_label, (width - 100, 5))
        draw_vector(screen, (width - 160, 30), np.array([[30.0], [0.0]]).flatten(), GREEN)
        vel_label = font.render("Acceleration", True, GREEN)
        screen.blit(vel_label, (width - 110, 25))

    #refresh
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
