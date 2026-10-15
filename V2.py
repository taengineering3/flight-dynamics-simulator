"""
Flight Dynamics Simulator - V2
Stage: 3D motion
"""

import plotly.graph_objects as go
import numpy as np

# ----- Aircraft & simulation parameters -----

mass = 1200.0        # kg
thrust = 5000.0      # Newtons, constant for now
drag_constant = 0.35 #(just a made-up value for now)
gravitational_constant = 9.81  # m/s^2, Earth's gravity 
air_density = 1.225 # kg/m^3, at sea level
wing_area = 20.0 # m^2
lift_coefficient = 0.3
side_force = 500

# ----- Initial conditions -----
velocity = np.array([0.0, 0.0, 0.0])
position = np.array([0.0, 0.0, 0.0])

# ----- Simulation settings -----
dt = 0.1          # seconds per step (how often we update)
total_time = 60.0 # simulate 60 seconds of flight
time = 0.0

# ----- Data storage for plotting later -----
time_history = []
velocity_history = []
position_history = []

# ----- Main simulation loop -----
while time < total_time:

    velocity_x = velocity[0]

    # Calculate drag force
    drag = drag_constant * velocity_x ** 2

    # Calculate lift force + weight force
    lift = 0.5 * air_density * velocity_x**2 * wing_area * lift_coefficient
    weight = mass * gravitational_constant
    lift = min(lift, weight)

    # Net Force
    weight_vector = np.array([0.0, -weight, 0.0])
    side_force_vector = np.array([0.0, 0.0, side_force])
    thrust_vector = np.array([thrust, 0.0, 0.0])
    drag_vector = np.array([-drag, 0.0, 0.0])
    lift_vector = np.array([0.0, lift, 0.0])

    net_force_vector = thrust_vector + drag_vector + lift_vector + weight_vector + side_force_vector


    # Acceleration + velocity + position
    acceleration = net_force_vector / mass
    velocity = velocity + acceleration * dt
    position = position + velocity * dt



    # STEP 6: Save this moment's data
    time_history.append(time)
    velocity_history.append(velocity.copy())
    position_history.append(position.copy())

    # STEP 7: Advance time
    time = time + dt

# ----- Print a quick summary -----
print(f"After {total_time} seconds:")
print(f"  Position: ({position[0]:.1f}, {position[1]:.1f}, {position[2]:.1f}) m")
print(f"  Velocity: ({velocity[0]:.1f}, {velocity[1]:.1f}, {velocity[2]:.1f}) m/s")
print(f"  Acceleration: ({acceleration[0]:.1f}, {acceleration[1]:.1f}, {acceleration[2]:.1f}) m/s^2")
print(f"  Lift: {lift:.1f} N, Weight: {weight:.1f} N")



# Plotting the 3D trajectory
x_vals = []
y_vals = []
z_vals = []

for pos in position_history:
    x_vals.append(pos[0])
    y_vals.append(pos[1])
    z_vals.append(pos[2])


fig = go.Figure(data=[go.Scatter3d(x=x_vals, y=y_vals, z=z_vals, mode='lines')])
go.Figure.update_layout(fig, title='3D Flight Trajectory', scene=dict(
    xaxis_title='X Position (m)',
    yaxis_title='Y Position (m)',
    zaxis_title='Z Position (m)'
))
fig.show()

