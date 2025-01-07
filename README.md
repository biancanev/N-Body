# N-Body

This is the documentation for my n-body Python simulator. This is a basic overview on how to use the simulator. For a full insight into the deisgn process, view [the design documentation](https://github.com/biancanev/N-Body/blob/main/N_Body_Documentation_rev1.pdf).

This simulation requires Python 3.10+.

### Basic Simulation

At the current iteration of the project, the only way to adjust parameters is to manually adjust the python code itself. A GUI implementation will be released soon to simplify the simulation process.

To use the simulator, run `python main.py`. The default simulation will be a 2 body orbital system. See Design Documentation Section 4.1 for more details on the default simulation.

The default numeric calculation method should be the constant acceleration method. The Verlet Integration method has been mostly implemented. To change this, change the `METHOD` constant to "VER" in `bodies.py`. More numeric methods will be added in future iterations of the project. See Design Documentation Sections 2 and 5.1.1 for more information about the different numerical methods. 

To add more bodies, you can instatiate more `Body` classes and add them to the `bodies` list in `main.py`. The default constructor is `Body(pos_x, pos_y, mass, vel_x, vel_y, color, radius)` where `pos_x` and `pos_y` are the inital position coordinates, `vel_x` and `vel_y` are the inital velocity values, `mass` is the mass of the body, `color` is the desired simulation color of the body and `radius` is the desired simulation radius of the body. For a full description of the `Body` class, see Design Documentation Section 3.1. 

### Stability

An important aspect of the simulator is the stability of the simulation. Large numeric values may cause the simulation to break, as Python may not be able to handle such large numbers. Stability scaling variables such as `mass_stability_scale` and `distance_stability_scale` have been implemented to reduce the effects of large scale simulations. Future implementations will automatically adjust these parameters to optimize visual simulation.
