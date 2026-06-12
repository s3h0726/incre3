import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Galaxy Conquest 3D", layout="wide")

# ----------------
# Save Data
# ----------------

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "fleet" not in st.session_state:
    st.session_state.fleet = 1

if "prestige" not in st.session_state:
    st.session_state.prestige = 0

if "planets" not in st.session_state:
    st.session_state.planets = []

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# ----------------
# Planet Data
# ----------------

PLANETS = [
    ("Earth", 0, 0, 0, 100),
    ("Mars", 10, 5, 2, 300),
    ("Europa", -8, 3, 7, 1000),
    ("Titan", 15, -10, 6, 3000),
    ("Kepler-22b", 25, 15, -5, 10000),
    ("Proxima b", -20, 20, 15, 25000),
    ("Andromeda Prime", 50, 50, 50, 100000),
]

# ----------------
# Idle Production
# ----------------

production = (
    10
    + st.session_state.fleet * 5
    + len(st.session_state.planets) * 20
    + st.session_state.prestige * 100
)

now = time.time()
delta = now - st.session_state.last_update

st.session_state.stars += int(delta * production)
st.session_state.last_update = now

# ----------------
# Header
# ----------------

st.title("🌌 Galaxy Conquest 3D")

c1, c2, c3, c4 = st.columns(4)

c1.metric("⭐ Stars", f"{st.session_state.stars:,}")
c2.metric("🚀 Fleet", st.session_state.fleet)
c3.metric("🪐 Planets", len(st.session_state.planets))
c4.metric("🌠 Prestige", st.session_state.prestige)

# ----------------
# 3D Galaxy Map
# ----------------

x = [p[1] for p in PLANETS]
y = [p[2] for p in PLANETS]
z = [p[3] for p in PLANETS]
labels = [p[0] for p in PLANETS]

fig = go.Figure()

fig.add_trace(
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers+text",
        text=labels,
        textposition="top center",
        marker=dict(
            size=8
        )
    )
)

fig.update_layout(
    height=600,
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# ----------------
# Conquest
# ----------------

st.subheader("🪐 Planet Conquest")

for name, px, py, pz, cost in PLANETS:

    owned = name in st.session_state.planets

    col1, col2 = st.columns([4,1])

    with col1:
        st.write(
            f"{name} | Cost: {cost:,}"
        )

    with col2:

        if owned:
            st.success("Owned")

        else:
            if st.button(
                f"Conquer {name}",
                key=name
            ):

                if st.session_state.stars >= cost:

                    st.session_state.stars -= cost

                    st.session_state.planets.append(
                        name
                    )

                    st.rerun()

# ----------------
# Fleet
# ----------------

st.subheader("🚀 Fleet")

fleet_cost = st.session_state.fleet * 100

if st.button(
    f"Build Fleet ({fleet_cost})"
):

    if st.session_state.stars >= fleet_cost:

        st.session_state.stars -= fleet_cost
        st.session_state.fleet += 1

        st.rerun()

# ----------------
# Prestige
# ----------------

need = 5 + st.session_state.prestige

st.subheader("🌠 Prestige")

st.write(
    f"Need {need} conquered planets"
)

if st.button("Ascend Civilization"):

    if len(st.session_state.planets) >= need:

        st.session_state.prestige += 1
        st.session_state.stars = 0
        st.session_state.fleet = 1
        st.session_state.planets = []

        st.rerun()

# ----------------
# Auto Refresh
# ----------------

time.sleep(1)
st.rerun()
