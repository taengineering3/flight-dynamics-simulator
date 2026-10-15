"""
Flight Dynamics Simulator - V1
Stage: 1D motion, thrust + drag only. No gravity, no lift, no 3D yet.
"""

# ----- Aircraft & simulation parameters -----

mass = 1200.0        # kg
thrust = 5000.0      # Newtons, constant for now
drag_constant = 0.35 #(just a made-up value for now)
gravitational_constant = 9.81  # m/s^2, Earth's gravity 
air_density = 1.225 # kg/m^3, at sea level
wing_area = 20.0 # m^2
lift_coefficient = 0.3

# ----- Initial conditions -----
velocity_x = 0.0
velocity_y = 0.0
position_x = 0.0
position_y = 0.0

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

    # Calculate drag force
    drag = drag_constant * velocity_x ** 2

    # Calculate lift force + weight force
    lift = 0.5 * air_density * velocity_x**2 * wing_area * lift_coefficient
    weight = mass * gravitational_constant
    lift = min(lift, weight)

    # Net Force
    net_force_x = thrust - drag
    net_force_y = lift - weight

    # Acceleration
    acceleration = net_force_x / mass
    acceleration_y = (lift - weight) / mass

    # STEP 4: Update velocity using acceleration
    velocity_x = velocity_x + acceleration * dt
    velocity_y = velocity_y + acceleration_y * dt

    # STEP 5: Update position using velocity
    position_x = position_x + velocity_x * dt
    position_y = position_y + velocity_y * dt

    # STEP 6: Save this moment's data
    time_history.append(time)
    velocity_history.append((velocity_x, velocity_y))
    position_history.append((position_x, position_y))

    # STEP 7: Advance time
    time = time + dt

# ----- Print a quick summary -----
print(f"After {total_time} seconds:")
print(f"  Position: ({position_x:.1f}, {position_y:.1f}) m")
print(f"  Velocity: ({velocity_x:.1f}, {velocity_y:.1f}) m/s")
print(f"  Acceleration: ({acceleration:.1f}, {acceleration_y:.1f}) m/s^2")
print(f"  Lift: {lift:.1f} N, Weight: {weight:.1f} N")