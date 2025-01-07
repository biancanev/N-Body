import numpy as np

"""
List of numerical methods:

CA - constant acceleration
VER(not yet implemented) - Verlet integration
RK4(not yet implemented) - 4th order Runge Kutte method
"""
VALID_METHODS = ["CA", "VER", "RK4"]
METHOD = "CA" #numerical method

assert METHOD in VALID_METHODS, 'Invalid numerical method given'

class Body:
    def __init__(self, x, y, m, v_x, v_y, color, r):
        x, y, v_x, v_y, m = float(x), float(y), float(v_x), float(v_y), float(m)
        self.position = np.array([[x],[y]])
        self.prev = np.array([[0.0],[0.0]])
        self.velocity = np.array([[v_x],[v_y]])
        self.acceleration = np.array([[0.0],[0.0]])
        self.mass = m
        self.color = color
        self.radius = r
        self.tracer = []

def calculate(bodies, g):
    for i, body in enumerate(bodies):
        F = np.array([[0.0],[0.0]])
        for j, other in enumerate(bodies):
            if i != j:
                pos = other.position - body.position
                mag = np.linalg.norm(pos)
                F += g * body.mass * other.mass / mag ** 3 * pos
        body.acceleration = F / body.mass
        print("Body", i, body.position.flatten())

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
                body.velocity = new_state[2:4]
        case _:
            print("Invalid numerical method")
