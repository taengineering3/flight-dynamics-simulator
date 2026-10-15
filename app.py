"""
Flight Dynamics Simulator - interactive web app (Streamlit)

Run locally with:   streamlit run app.py
"""

import plotly.graph_objects as go
import streamlit as st

from simulation import run_simulation

st.set_page_config(page_title="Flight Dynamics Simulator", layout="wide")

st.title("✈️ Flight Dynamics Simulator")
st.caption(
    "V2: 3D point-mass flight under thrust, drag, lift and gravity. "
    "Change the parameters on the left and the simulation re-runs instantly. "
    "Work in progress: control surfaces (V3), realistic aerodynamics (V4) and an autopilot (V5) are planned."
)

# ----- Sidebar: inputs -----
st.sidebar.header("Aircraft")
mass = st.sidebar.slider("Mass (kg)", 500.0, 5000.0, 1200.0, 50.0)
wing_area = st.sidebar.slider("Wing area (m²)", 5.0, 60.0, 20.0, 1.0)
lift_coefficient = st.sidebar.slider("Lift coefficient", 0.0, 1.5, 0.3, 0.05)
drag_constant = st.sidebar.slider("Drag constant k (Drag = k·v²)", 0.05, 2.0, 0.35, 0.05)

st.sidebar.header("Forces")
thrust = st.sidebar.slider("Thrust (N)", 0.0, 20000.0, 5000.0, 250.0)
side_force = st.sidebar.slider("Side force (N)", -2000.0, 2000.0, 500.0, 50.0)

st.sidebar.header("Initial conditions")
initial_speed = st.sidebar.slider("Initial forward speed (m/s)", 0.0, 200.0, 0.0, 5.0)
initial_altitude = st.sidebar.slider("Initial altitude (m)", 0.0, 10000.0, 0.0, 100.0)

st.sidebar.header("Simulation")
total_time = st.sidebar.slider("Duration (s)", 10.0, 300.0, 60.0, 10.0)
dt = st.sidebar.select_slider("Time step dt (s)", options=[0.01, 0.05, 0.1, 0.2, 0.5], value=0.1)

# ----- Run -----
result = run_simulation(
    mass=mass,
    thrust=thrust,
    drag_constant=drag_constant,
    wing_area=wing_area,
    lift_coefficient=lift_coefficient,
    side_force=side_force,
    initial_speed=initial_speed,
    initial_altitude=initial_altitude,
    total_time=total_time,
    dt=dt,
)
t = result["time"]
pos = result["position"]
vel = result["velocity"]

# ----- Summary numbers -----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Final altitude", f"{pos[-1, 1]:,.0f} m")
c2.metric("Distance forward", f"{pos[-1, 0]:,.0f} m")
c3.metric("Sideways drift", f"{pos[-1, 2]:,.0f} m")
c4.metric("Final forward speed", f"{vel[-1, 0]:.1f} m/s")

# ----- 3D trajectory -----
# Simulation axes: x forward, y up, z sideways.
# Plotly's vertical axis is z, so we plot (x, z_sim, y_sim) to keep altitude vertical.
fig3d = go.Figure(
    data=[
        go.Scatter3d(
            x=pos[:, 0], y=pos[:, 2], z=pos[:, 1],
            mode="lines", line=dict(width=5, color=t, colorscale="Viridis",
                                    colorbar=dict(title="Time (s)")),
            name="Trajectory",
        ),
        go.Scatter3d(
            x=[pos[0, 0]], y=[pos[0, 2]], z=[pos[0, 1]],
            mode="markers", marker=dict(size=6, color="green"), name="Start",
        ),
        go.Scatter3d(
            x=[pos[-1, 0]], y=[pos[-1, 2]], z=[pos[-1, 1]],
            mode="markers", marker=dict(size=6, color="red"), name="End",
        ),
    ]
)
fig3d.update_layout(
    title="3D flight trajectory",
    height=600,
    margin=dict(l=0, r=0, t=40, b=0),
    scene=dict(
        xaxis_title="Forward x (m)",
        yaxis_title="Sideways z (m)",
        zaxis_title="Altitude y (m)",
        aspectmode="auto",
    ),
)
st.plotly_chart(fig3d, width="stretch")

# ----- Time-series plots -----
left, right = st.columns(2)

fig_alt = go.Figure(go.Scatter(x=t, y=pos[:, 1], mode="lines"))
fig_alt.update_layout(title="Altitude vs time", xaxis_title="Time (s)",
                      yaxis_title="Altitude (m)", height=350)
left.plotly_chart(fig_alt, width="stretch")

fig_vel = go.Figure()
fig_vel.add_trace(go.Scatter(x=t, y=vel[:, 0], mode="lines", name="Forward (x)"))
fig_vel.add_trace(go.Scatter(x=t, y=vel[:, 1], mode="lines", name="Vertical (y)"))
fig_vel.add_trace(go.Scatter(x=t, y=vel[:, 2], mode="lines", name="Sideways (z)"))
fig_vel.update_layout(title="Velocity components vs time", xaxis_title="Time (s)",
                      yaxis_title="Velocity (m/s)", height=350)
right.plotly_chart(fig_vel, width="stretch")

with st.expander("About the model (V2 simplifications)"):
    st.markdown(
        """
- The aircraft is a **point mass**: no rotation (pitch/roll/yaw) yet.
- **Thrust** and **side force** are constant forces; **drag** = k·v²;
  **lift** = ½·ρ·v²·S·C_L, capped so it can never exceed weight.
- The lift cap is a deliberate V1 simplification. Without angle of attack and stall
  modelling, the aircraft cannot hold a target altitude, so it keeps whatever climb or
  sink rate it built up before lift balanced weight.
- Altitude can go negative: there is no ground in the model yet.
- Integration is explicit Euler with time step dt.
"""
    )
