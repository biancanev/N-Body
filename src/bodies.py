import numpy as np
import json

"""
List of numerical methods:

CA - constant acceleration
VER - Verlet integration
RK4(not yet implemented) - 4th order Runge Kutte method
"""
VALID_METHODS = ["CA", "VER", "RK4"]
METHOD = "VER" #numerical method

#load user-defined configuration
try:
    config = json.load(open("simulation_config.json"))
except:
    config = {
    "km_per_pixel" : 200,
    "mass_stability_scale" : 1e-15,
    "distance_stability_scale" : 10,
    "G" : 6.67e-11,
    "dt" : 2 ,
    "TRACER" : True,
    "LOGGING" : False,
    "bodies" : []
    }
    print("ERROR: Could not load simualtion_config.json. Using default parameters instead.")

#Constants for simulation as defined by config json(may change later to only rely on the dictionary read by json)
km_per_pixel = config["km_per_pixel"] if "km_per_pixel" in config else 200
m_per_pixel = km_per_pixel * 1000
mass_stability_scale = config["mass_stability_scale"] if "mass_stability_scale" in config else 1e-15
distance_stability_scale = config["distance_stability_scale"] if "distance_stability_scale" in config else 10
G = config["G"] if "G" in config else 6.67e-11 #expressed in m^3/(kg*s^2)
G_SCALED = G * (m_per_pixel ** 3) * mass_stability_scale
dt = config["dt"] if "dt" in config else 2#expressed in seconds
TRACER = config["TRACER"] if "TRACER" in config else True
LOGGING = config["LOGGING"] if "LOGGING" in config else False

#sanity check
assert METHOD in VALID_METHODS, 'Invalid numerical method given'

"""
Body class. This is the object that represents a body in motion.

TODO:
 - Account for angular momentum/velocity
"""
class Body:
    def __init__(self, x, y, m, v_x, v_y, color, r):
        x, y, v_x, v_y, m = float(x), float(y), float(v_x), float(v_y), float(m)
        self.position = np.array([[x],[y]])
        self.velocity = np.array([[v_x],[v_y]])
        self.prev = np.array([[0.0],[0.0]])
        self.acceleration = np.array([[0.0],[0.0]])
        self.mass = m
        self.color = color
        self.radius = r
        self.tracer = []
    
    def status(self):
        return f"pos:{self.position.flatten()}, prev:{self.prev.flatten()}, vel:{self.velocity.flatten()}, acc:{self.acceleration.flatten()}"

"""
Calculate the net force exerted on every body and change acceleration accordingly

TODO:
 - Account for angular momentum/velocity
 - Optimize for computational efficiency
"""
def calculate(bodies, g):
    for i, body in enumerate(bodies):
        F = np.array([[0.0],[0.0]])
        for j, other in enumerate(bodies):
            if i != j:
                pos = other.position - body.position
                mag = np.linalg.norm(pos)
                F += g * body.mass * other.mass / mag ** 3 * pos
        body.acceleration = sanitize_values(F / body.mass)
        #print("DEBUG: Body", i, body.status())

"""
Update an object's position and velocity based on the changed acceleration calculated by calculate()

TODO:
 - Add RK4 method
 - Account for angular momentum/velocity
"""
def update(bodies, dt):
    match METHOD:
        case "CA":
            T = np.array([
                [1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

            for body in bodies:
                state = np.vstack((body.position, body.velocity))
                a = np.vstack((body.acceleration, body.acceleration)) * dt ** 2 / 2
                new_state = np.matmul(T, state) + a
                body.position = new_state[:2]
                body.velocity = new_state[2:]
        case "VER":
            T = np.array([[2, 0, -1, 0, dt**2, 0],
                         [0, 2, 0, -1, 0, dt**2],
                         [1, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1]
                         ])
            for body in bodies:
                state = np.vstack((body.position, body.prev))
                state = np.vstack((state, body.acceleration))
                new_state = np.matmul(T, state)
                body.prev = body.position
                body.position = new_state[:2]
                body.velocity = (body.position - body.prev) / (2 * dt)
        case _:
            print("Invalid numerical method")

"""
In case of extremely small values, default to 0 to ensure no floating point errors
"""
def sanitize_values(array, thresh=1e-10):
    return np.where(np.abs(array) < thresh, 0, array)

"""
Check for collisions in the simulation and apply conservation of momentum

TODO:
 - Handle multi-body collisions
 - Account for angular momentum
"""
def handle_colision(body1, body2, bodies, g, dt):
    dist = np.linalg.norm(body1.position - body2.position)
    if dist < body1.radius + body2.radius:
        new_mass = body1.mass + body2.mass
        new_pos = sanitize_values((body1.position * body1.mass + body2.position * body2.mass) / new_mass)
        new_vel = sanitize_values((body1.velocity * body1.mass + body2.velocity * body2.mass) / new_mass)
        body1.position = new_pos
        body1.velocity = new_vel
        body1.mass = new_mass
        body1.radius = int((body1.radius**3 + body2.radius**3)**(1/3))
        bodies.remove(body2)
        body1.acceleration = np.zeros_like(body1.acceleration)
        body1.prev = body1.position - body1.velocity * dt
        calculate(bodies, g)