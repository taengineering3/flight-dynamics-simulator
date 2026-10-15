# Flight Dynamics Simulator

A Python simulator that models an aircraft's motion through 3D space from first principles
(Newton's second law, numerical integration), with an interactive web interface.

**Status: work in progress.** V1 and V2 are complete; V3 is in development.

## What it does

- Computes the aircraft's position and velocity over time under **thrust, drag, lift and gravity**
- Tracks full **3D motion** (x forward, y altitude, z sideways) using NumPy vectors
- Provides an **interactive Streamlit app**: change mass, thrust, wing area, drag, initial conditions
  and see the 3D trajectory and time plots update instantly

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

To just print the default simulation result in the terminal:

```bash
python simulation.py
```

## How the physics works

Every time step `dt`, the simulator repeats this loop:

```
state (position, velocity)
   -> compute forces (thrust, drag, lift, weight, side force)
   -> net force / mass = acceleration        (a = F / m)
   -> velocity += acceleration * dt
   -> position += velocity * dt
   -> store the state, advance time
```

| Force  | Model                                  |
|--------|----------------------------------------|
| Thrust | constant (for now)                     |
| Drag   | `k * v^2`                              |
| Lift   | `0.5 * rho * v^2 * S * C_L`, capped at weight |
| Weight | `m * g`                                |

The simulation was validated against analytical results (free fall: `y = 1/2 g t^2`, `v = g t`)
and reproduces terminal velocity when thrust and drag balance.

## Roadmap

- [x] **V1** Physics engine: thrust, drag, lift, gravity, validated against theory
- [x] **V2** 3D motion, NumPy vectorization, interactive Plotly + Streamlit visualization
- [ ] **V3** Control inputs: throttle, elevator, ailerons, rudder; pitch/roll/yaw
- [ ] **V4** Realistic aerodynamics: angle of attack, stall, dynamic pressure, C_L / C_D / moment coefficients
- [ ] **V5** PID autopilot holding target altitude, heading and speed

## Known simplifications (V2)

- Point-mass model: no rotation yet
- Constant lift coefficient, lift capped at weight (no angle of attack or stall)
- Constant air density, no ground contact (altitude can go negative)
- Explicit Euler integration

## Project structure

```
flight-dynamics-simulator/
├── simulation.py      # physics engine: run_simulation(...)
├── app.py             # Streamlit interface
├── requirements.txt
└── README.md
```

## Stack

Python, NumPy, Plotly, Streamlit
