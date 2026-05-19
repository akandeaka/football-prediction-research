import os, json
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            source TEXT DEFAULT 'betmines',
            home_team TEXT,
            away_team TEXT,
            home_odds FLOAT,
            draw_odds FLOAT,
            away_odds FLOAT,
            prediction JSONB,
            actual_result TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_prediction(match):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO predictions (source, home_team, away_team, home_odds, draw_odds, away_odds, prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        match.get("source", "betmines"),
        match["home_team"],
        match["away_team"],
        match["home_odds"],
        match["draw_odds"],
        match["away_odds"],
        json.dumps(match["prediction"])
    ))
    conn.commit()
    cur.close()
    conn.close()

def update_result(home_team, away_team, result):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE predictions
        SET actual_result = %s
        WHERE home_team = %s AND away_team = %s AND actual_result IS NULL
    """, (result, home_team, away_team))
    conn.commit()
    cur.close()
    conn.close()

def calculate_accuracy():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FILTER (WHERE prediction->>'winner' = actual_result) AS correct,
               COUNT(*) AS total
        FROM predictions
        WHERE actual_result IS NOT NULL
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row["total"] > 0:
        return round((row["correct"] / row["total"]) * 100, 2)
    return 0.0
