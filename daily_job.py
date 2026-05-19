from scraper import get_worldwide_predictions, fetch_match_result
from db import init_db, save_prediction, update_result

def run_daily():
    init_db()
    data = get_worldwide_predictions()
    for match in data:
        save_prediction(match)
        result = fetch_match_result(match["url"])
        if result:
            update_result(match["home_team"], match["away_team"], result)
    print(f"Processed {len(data)} matches with automated validation")

if __name__ == "__main__":
    run_daily()
