import json
import os
import random

SAVE_FILE = "save.json"

PLANETS = [
    {"name": "Earth", "galaxy": "Milky Way", "cost": 100},
    {"name": "Mars", "galaxy": "Milky Way", "cost": 250},
    {"name": "Proxima Centauri b", "galaxy": "Milky Way", "cost": 500},
    {"name": "Kepler-22b", "galaxy": "Milky Way", "cost": 1000},
    {"name": "Andromeda Prime", "galaxy": "Andromeda", "cost": 2500},
    {"name": "M31-X", "galaxy": "Andromeda", "cost": 5000},
    {"name": "Triangulum One", "galaxy": "Triangulum", "cost": 10000},
    {"name": "M87 Prime", "galaxy": "Messier 87", "cost": 25000},
    {"name": "IC-1101A", "galaxy": "IC 1101", "cost": 50000},
    {"name": "Centaurus A-7", "galaxy": "Centaurus A", "cost": 100000},
]

RESEARCH = {
    "채굴 드론": {"cost": 500, "bonus": 2},
    "AI 채굴": {"cost": 3000, "bonus": 5},
    "양자 채굴": {"cost": 15000, "bonus": 10},
}

def new_save():
    return {
        "stars": 0,
        "fleet": 1,
        "prestige": 0,
        "research": [],
        "planets": [],
        "total_conquered": 0
    }

def load():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return new_save()

def save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def mining_power(data):
    power = 10

    power += len(data["planets"]) * 5
    power += data["fleet"] * 3
    power += data["prestige"] * 25

    for r in data["research"]:
        power *= RESEARCH[r]["bonus"]

    return power

def prestige_requirement(data):
    return 5 + data["prestige"] * 3

def prestige(data):
    need = prestige_requirement(data)

    if len(data["planets"]) < need:
        print(f"\n❌ 프레스티지 조건 부족 ({len(data['planets'])}/{need})")
        return

    data["prestige"] += 1
    data["stars"] = 0
    data["fleet"] = 1
    data["research"] = []
    data["planets"] = []

    print("\n🌌 문명 승천 성공!")
    print(f"프레스티지 레벨: {data['prestige']}")

def build_fleet(data):
    cost = data["fleet"] * 100

    if data["stars"] < cost:
        print("자원 부족")
        return

    data["stars"] -= cost
    data["fleet"] += 1

    print(f"🚀 함대 +1 (현재 {data['fleet']})")

def conquer(data):
    available = [p for p in PLANETS if p["name"] not in data["planets"]]

    if not available:
        print("모든 행성 정복 완료")
        return

    print("\n=== 정복 가능 행성 ===")

    for i, p in enumerate(available, 1):
        print(
            f"{i}. {p['name']} "
            f"({p['galaxy']}) "
            f"비용:{p['cost']}"
        )

    try:
        idx = int(input("번호 선택: ")) - 1
        target = available[idx]

        if data["stars"] < target["cost"]:
            print("자원 부족")
            return

        chance = min(
            95,
            40 + data["fleet"] * 5
        )

        if random.randint(1, 100) <= chance:
            data["stars"] -= target["cost"]
            data["planets"].append(target["name"])
            data["total_conquered"] += 1

            print(f"✅ {target['name']} 정복 성공")
        else:
            data["stars"] -= target["cost"] // 2
            print("💥 침공 실패")

    except:
        print("잘못된 입력")

def research(data):
    print("\n=== 연구 ===")

    for name, info in RESEARCH.items():
        if name not in data["research"]:
            print(
                f"- {name} "
                f"(비용 {info['cost']})"
            )

    target = input("연구 이름: ")

    if target not in RESEARCH:
        return

    if target in data["research"]:
        return

    cost = RESEARCH[target]["cost"]

    if data["stars"] < cost:
        print("자원 부족")
        return

    data["stars"] -= cost
    data["research"].append(target)

    print("🔬 연구 완료")

def show_stats(data):
    print("\n========================")
    print("은하 제국 현황")
    print("========================")
    print("⭐ 자원:", data["stars"])
    print("🚀 함대:", data["fleet"])
    print("🌌 프레스티지:", data["prestige"])
    print("🪐 정복 행성:", len(data["planets"]))
    print("🏆 총 정복:", data["total_conquered"])
    print("⛏ 채굴력:", mining_power(data))
    print("========================")

def mine(data):
    gain = mining_power(data)
    data["stars"] += gain

    print(f"\n⭐ +{gain} 자원")

def main():
    data = load()

    while True:
        show_stats(data)

        print("""
1. 자원 채굴
2. 함대 건조
3. 행성 정복
4. 연구
5. 프레스티지
6. 저장
7. 종료
""")

        cmd = input("> ")

        if cmd == "1":
            mine(data)

        elif cmd == "2":
            build_fleet(data)

        elif cmd == "3":
            conquer(data)

        elif cmd == "4":
            research(data)

        elif cmd == "5":
            prestige(data)

        elif cmd == "6":
            save(data)
            print("저장 완료")

        elif cmd == "7":
            save(data)
            print("게임 종료")
            break

if __name__ == "__main__":
    main()
