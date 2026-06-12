import streamlit as st
import time

st.set_page_config(page_title="Galaxy Conquest", page_icon="🌌", layout="wide")

# -----------------
# 초기 데이터
# -----------------

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "fleet" not in st.session_state:
    st.session_state.fleet = 1

if "prestige" not in st.session_state:
    st.session_state.prestige = 0

if "research" not in st.session_state:
    st.session_state.research = []

if "planets" not in st.session_state:
    st.session_state.planets = []

if "achievements" not in st.session_state:
    st.session_state.achievements = []

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()

# -----------------
# 데이터
# -----------------

PLANETS = [
    ("Earth", "Milky Way", 100),
    ("Mars", "Milky Way", 250),
    ("Europa", "Milky Way", 500),
    ("Titan", "Milky Way", 1000),
    ("Kepler-22b", "Milky Way", 2500),
    ("Proxima Centauri b", "Milky Way", 5000),
    ("Andromeda Prime", "Andromeda", 10000),
    ("M31-X", "Andromeda", 25000),
    ("Triangulum One", "Triangulum", 50000),
    ("M87 Prime", "Messier 87", 100000),
    ("IC-1101A", "IC 1101", 250000),
    ("Centaurus-A7", "Centaurus A", 500000),
]

RESEARCH = {
    "Mining Drones": (1000, 2),
    "Quantum Mining": (5000, 5),
    "Dyson Swarm": (25000, 10),
    "AI Civilization": (100000, 25),
}

# -----------------
# 자동 생산
# -----------------

def mining_power():
    power = (
        10
        + st.session_state.fleet * 3
        + len(st.session_state.planets) * 5
        + st.session_state.prestige * 50
    )

    for r in st.session_state.research:
        power *= RESEARCH[r][1]

    return int(power)

now = time.time()
elapsed = now - st.session_state.last_tick

if elapsed >= 1:
    st.session_state.stars += int(mining_power() * elapsed)
    st.session_state.last_tick = now

# -----------------
# 업적
# -----------------

if len(st.session_state.planets) >= 1 and "첫 정복" not in st.session_state.achievements:
    st.session_state.achievements.append("첫 정복")

if len(st.session_state.planets) >= 5 and "우주 개척자" not in st.session_state.achievements:
    st.session_state.achievements.append("우주 개척자")

if st.session_state.prestige >= 1 and "문명 승천" not in st.session_state.achievements:
    st.session_state.achievements.append("문명 승천")

# -----------------
# UI
# -----------------

st.title("🌌 Galaxy Conquest")

c1, c2, c3, c4 = st.columns(4)

c1.metric("⭐ 자원", f"{st.session_state.stars:,}")
c2.metric("🚀 함대", st.session_state.fleet)
c3.metric("🪐 행성", len(st.session_state.planets))
c4.metric("🌠 프레스티지", st.session_state.prestige)

st.progress(min(len(st.session_state.planets) / 12, 1.0))

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["채굴", "함대", "정복", "연구", "프레스티지"]
)

# -----------------
# 채굴
# -----------------

with tab1:
    st.subheader("자원 생산")

    st.write("초당 생산량:", mining_power())

    if st.button("⛏ 즉시 채굴"):
        st.session_state.stars += mining_power()
        st.rerun()

# -----------------
# 함대
# -----------------

with tab2:
    st.subheader("함대")

    fleet_cost = st.session_state.fleet * 100

    st.write("건조 비용:", fleet_cost)

    if st.button("🚀 함대 건조"):
        if st.session_state.stars >= fleet_cost:
            st.session_state.stars -= fleet_cost
            st.session_state.fleet += 1
            st.rerun()

# -----------------
# 정복
# -----------------

with tab3:
    st.subheader("행성 정복")

    for name, galaxy, cost in PLANETS:

        owned = name in st.session_state.planets

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"🪐 {name} | {galaxy} | 비용 {cost:,}"
            )

        with col2:

            if owned:
                st.success("소유")

            else:
                if st.button(
                    f"정복 {name}",
                    key=name
                ):
                    if st.session_state.stars >= cost:
                        st.session_state.stars -= cost
                        st.session_state.planets.append(name)
                        st.rerun()

# -----------------
# 연구
# -----------------

with tab4:
    st.subheader("기술 연구")

    for name, info in RESEARCH.items():

        cost = info[0]

        if name in st.session_state.research:
            st.success(name)

        else:
            if st.button(
                f"{name} ({cost:,})",
                key=f"research_{name}"
            ):
                if st.session_state.stars >= cost:
                    st.session_state.stars -= cost
                    st.session_state.research.append(name)
                    st.rerun()

# -----------------
# 프레스티지
# -----------------

with tab5:

    need = 5 + st.session_state.prestige * 3

    st.write(
        f"필요 행성 수: {need}"
    )

    if st.button("🌠 문명 승천"):

        if len(st.session_state.planets) >= need:

            st.session_state.prestige += 1

            st.session_state.stars = 0
            st.session_state.fleet = 1
            st.session_state.planets = []
            st.session_state.research = []

            st.rerun()

# -----------------
# 사이드바
# -----------------

with st.sidebar:

    st.header("🏆 업적")

    if st.session_state.achievements:
        for a in st.session_state.achievements:
            st.success(a)
    else:
        st.write("없음")

    st.header("📊 통계")

    st.write("초당 생산:", mining_power())
    st.write("연구 수:", len(st.session_state.research))
    st.write("정복 수:", len(st.session_state.planets))
