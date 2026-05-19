import requests
from bs4 import BeautifulSoup
from prediction_engine import PredictionEngine

HEADERS = {"User-Agent": "Mozilla/5.0"}
engine = PredictionEngine("rule_engine.json")

def fetch_betmines_worldwide():
    url = "https://www.betmines.com/football/today"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []
    for row in soup.select("a[href*='/matches/predictions-']"):
        teams = row.select("p.tw-font-semibold")
        odds = row.select("div.tw-w-14 span")

        if len(teams) >= 2 and len(odds) >= 3:
            home_team = teams[0].get_text(strip=True)
            away_team = teams[1].get_text(strip=True)
            home_odds = float(odds[0].get_text(strip=True))
            draw_odds = float(odds[1].get_text(strip=True))
            away_odds = float(odds[2].get_text(strip=True))

            matches.append({
                "home_team": home_team,
                "away_team": away_team,
                "home_odds": home_odds,
                "draw_odds": draw_odds,
                "away_odds": away_odds,
                "url": row["href"]
            })
    return matches

def fetch_match_result(match_url):
    full_url = f"https://www.betmines.com{match_url}"
    r = requests.get(full_url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    score_block = soup.select_one("p.tw-text-bm-gray-font-4")
    if score_block:
        score_text = score_block.get_text(strip=True)
        if "-" in score_text:
            home_goals, away_goals = [int(x.strip()) for x in score_text.split("-")]
            if home_goals > away_goals:
                return "home"
            elif home_goals < away_goals:
                return "away"
            else:
                return "draw"
    return None

def get_worldwide_predictions():
    raw_matches = fetch_betmines_worldwide()
    results = []
    for m in raw_matches:
        match_input = {
            "home_odds": m["home_odds"],
            "draw_odds": m["draw_odds"],
            "away_odds": m["away_odds"],
            "competition_tag": None
        }
        pred = engine.predict(match_input)
        m["prediction"] = pred
        results.append(m)
    return results
