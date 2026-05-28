"""
DNA診断v2 メインオーケストレーター（lunar-python + skyfield統合・精度向上版）
"""
from datetime import date, datetime
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculations.numerology import life_path_number, birth_day_number, destiny_number_from_name
from calculations.western_astrology import get_sun_sign, get_moon_sign, get_ascendant
from calculations.kyusei import honmei_star, gekkimei_star
from calculations.shichuusuimei import year_pillar, month_pillar, day_pillar, hour_pillar
from calculations.doubutsu_teiou import get_doubutsu_kyara, get_teiougaku, get_shusei
from calculations.personality_quiz import calculate_mbti, calculate_wd
from calculations.tenchuusatsu import get_tenchusatsu, get_year_fortune, get_tenchusatsu_years, get_multi_year_fortune
from pdf_generator import generate_pdf


def run_diagnosis(user_input: dict) -> dict:
    bd_str = user_input["birth_date"]
    year, month, day = [int(x) for x in bd_str.split("-")]
    bt = user_input.get("birth_time", "12:00")
    birth_hour = int(bt.split(":")[0])
    birth_minute = int(bt.split(":")[1]) if ":" in bt else 0

    # 出生地（デフォルト東京、サラさんは長崎）
    lat = user_input.get("lat", 35.6762)
    lon = user_input.get("lon", 139.6503)

    result = {
        "numerology": {
            "life_path": life_path_number(year, month, day),
            "birth_day": birth_day_number(day),
            "destiny": destiny_number_from_name(user_input.get("name_kana", "")),
        },
        "western_astrology": {
            "sun": get_sun_sign(year, month, day, birth_hour, birth_minute),
            "moon": get_moon_sign(year, month, day, birth_hour, birth_minute),
            "asc": get_ascendant(year, month, day, birth_hour, birth_minute, lat, lon),
        },
        "kyusei": {
            "honmei": honmei_star(year),
            "gekkimei": gekkimei_star(year, month),
        },
        "shichuusuimei": {
            "year": year_pillar(year, month, day),
            "month": month_pillar(year, month, day),
            "day": day_pillar(year, month, day),
            "hour": hour_pillar(year, month, day, birth_hour, birth_minute),
        },
        "doubutsu": get_doubutsu_kyara(year, month, day),
        "shusei": get_shusei(year, month, day),
        "teiou": get_teiougaku(year, month, day),
        "personality": {
            "mbti": calculate_mbti(user_input.get("answers", {})),
            "wd": calculate_wd(user_input.get("answers", {})),
        },
        "fortune": get_year_fortune(year, month, day),
        "fortune_3years": get_multi_year_fortune(year, month, day, datetime.now().year, datetime.now().year + 2),
        "tenchusatsu_years": get_tenchusatsu_years(year, month, day),
    }
    return result


def main():
    sara_input = {
        "name": "山岡 サラ",
        "name_kana": "ヤマオカサラ",
        "birth_date": "1963-07-31",
        "birth_time": "06:00",
        "birth_place": "長崎県 長崎市",
        "lat": 32.75,
        "lon": 129.88,
        "answers": {
            "Q1": "A", "Q2": "A",
            "Q3": "B", "Q4": "B",
            "Q5": "B", "Q6": "B",
            "Q7": "B", "Q8": "B",
            "WD1": "A",
        }
    }

    print("=== 計算開始 ===")
    result = run_diagnosis(sara_input)

    print("\n--- 計算結果（主要） ---")
    print(f"日柱: {result['shichuusuimei']['day']['kanshi']}")
    print(f"動物キャラ: {result['doubutsu']['name_60']}")
    print(f"算命学主星: {result['shusei']['name']}")
    print(f"月星座: {result['western_astrology']['moon']['name']}")

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"DNA診断_{sara_input['name'].replace(' ', '')}_v3.1_{datetime.now().strftime('%Y%m%d')}.pdf")

    print(f"\n=== PDF生成中: {output_path} ===")
    generate_pdf(sara_input, result, output_path)
    print("=== 完了 ===")


if __name__ == "__main__":
    main()
