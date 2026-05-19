import json

class PredictionEngine:
    def __init__(self, rules_file):
        with open(rules_file) as f:
            self.rules = json.load(f)

    def predict(self, match_input):
        # Simple rule: lowest odds = predicted winner
        odds = {
            "home": match_input["home_odds"],
            "draw": match_input["draw_odds"],
            "away": match_input["away_odds"]
        }
        winner = min(odds, key=odds.get)
        return {"winner": winner, "odds": odds}
