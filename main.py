import json
import os

SAVE_FILE = "save.json"

PLANETS = [
    ("Earth", 100),
    ("Mars", 300),
    ("Europa", 800),
    ("Titan", 2000),
    ("Kepler-22b", 5000),
    ("Proxima b", 12000),
    ("Andromeda Prime", 30000),
    ("Triangulum One", 80000),
]

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return {
        "stars": 0,
        "fleet": 1,
        "prestige": 0,
        "planets": []
    }

def save_game(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def mining_power(data):
    return (
        10
        + data["fleet"] * 5
        + len(data["planets"]) * 20
        + data["prestige"] * 100
    )

def show_status(data):
    print("\n" + "=" * 40)
    print("GALAXY CONQUEST")
    print("=" * 40)
    print("⭐ 자원:", data["stars"])
    print("🚀 함대:", data["fleet"])
    print("🌌 프레스티지:", data["prestige"])
    print("🪐 정복 행성:", len(data["planets"]))
    print("⛏ 채굴력:", mining_power(data))
    print("=" * 40)

def mine(data):
    gain = mining_power(data)
    data["stars"] += gain
    print(f"+{gain} 자원 획득")

def build_fleet(data):
    cost = data["fleet"] * 50

    if data["stars"] < cost:
        print("자원이 부족합니다.")
        return

    data["stars"] -= cost
    data["fleet"] += 1

    print("함대 건조 완료")

def conquer(data):
    available = []

    for planet, cost in PLANETS:
        if planet not in data["planets"]:
            available.append((planet, cost))

    if not available:
        print("모든 행성을 정복했습니다.")
        return

    print("\n정복 가능한 행성")

    for i, (planet, cost) in enumerate(available, start=1):
        print(f"{i}. {planet} (비용 {cost})")

    try:
        choice = int(input("번호 선택: ")) - 1

        planet, cost = available[choice]

        if data["stars"] < cost:
            print("자원이 부족합니다.")
            return

        data["stars"] -= cost
        data["planets"].append(planet)

        print(f"{planet} 정복 성공!")

    except:
        print("잘못된 입력")

def prestige(data):
    need = 5 + data["prestige"] * 3

    if len(data["planets"]) < need:
        print(f"행성 {need}개 필요")
        return

    data["prestige"] += 1
    data["stars"] = 0
    data["fleet"] = 1
    data["planets"] = []

    print("🌌 프레스티지 성공!")

def main():
    data = load_game()

    while True:
        show_status(data)

        print("""
1. 자원 채굴
2. 함대 건조
3. 행성 정복
4. 프레스티지
5. 저장
6. 종료
""")

        choice = input("> ")

        if choice == "1":
            mine(data)

        elif choice == "2":
            build_fleet(data)

        elif choice == "3":
            conquer(data)

        elif choice == "4":
            prestige(data)

        elif choice == "5":
            save_game(data)
            print("저장 완료")

        elif choice == "6":
            save_game(data)
            print("게임 종료")
            break

        else:
            print("잘못된 입력")

if __name__ == "__main__":
    main()
