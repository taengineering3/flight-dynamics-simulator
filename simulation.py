"""
Flight Dynamics Simulator - V2
Core physics engine: 3D motion under thrust, drag, lift (capped) and gravity.

Axis convention:
    x = forward, y = up (altitude), z = sideways
"""

import numpy as np


def run_simulation(
    mass=1200.0,                # kg
    thrust=5000.0,              # N, constant for now
    drag_constant=0.35,         # k in Drag = k * v^2 (placeholder value)
    wing_area=20.0,             # m^2
    lift_coefficient=0.3,       # simplified, constant (angle of attack comes in V4)
    side_force=500.0,           # N, constant placeholder (rudder/yaw replaces this in V3)
    air_density=1.225,          # kg/m^3, sea level
    gravity=9.81,               # m/s^2
    initial_speed=0.0,          # m/s, forward speed at t = 0
    initial_altitude=0.0,       # m
    total_time=60.0,            # s
    dt=0.1,                     # s per step
):
    """Run the simulation and return the time history as NumPy arrays."""

    velocity = np.array([initial_speed, 0.0, 0.0])
    position = np.array([0.0, initial_altitude, 0.0])

    time = 0.0
    time_history = []
    velocity_history = []
    position_history = []

    while time < total_time:

        velocity_x = velocity[0]

        # Scalar force magnitudes
        drag = drag_constant * velocity_x ** 2
        lift = 0.5 * air_density * velocity_x ** 2 * wing_area * lift_coefficient
        weight = mass * gravity
        lift = min(lift, weight)  # V1 simplification: lift can never exceed weight

        # Force vectors
        thrust_vector = np.array([thrust, 0.0, 0.0])
        drag_vector = np.array([-drag, 0.0, 0.0])
        lift_vector = np.array([0.0, lift, 0.0])
        weight_vector = np.array([0.0, -weight, 0.0])
        side_force_vector = np.array([0.0, 0.0, side_force])

        net_force = (thrust_vector + drag_vector + lift_vector
                     + weight_vector + side_force_vector)

        # Newton's second law, then integrate
        acceleration = net_force / mass
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        time_history.append(time)
        velocity_history.append(velocity.copy())
        position_history.append(position.copy())

        time = time + dt

    return {
        "time": np.array(time_history),
        "velocity": np.array(velocity_history),
        "position": np.array(position_history),
    }


if __name__ == "__main__":
    # Quick check with the default aircraft
    result = run_simulation()
    pos = result["position"][-1]
    vel = result["velocity"][-1]
    print("After 60.0 seconds:")
    print(f"  Position: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}) m")
    print(f"  Velocity: ({vel[0]:.1f}, {vel[1]:.1f}, {vel[2]:.1f}) m/s")
