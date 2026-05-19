import streamlit as st
from scraper import get_worldwide_predictions
from db import calculate_accuracy

st.title("Worldwide Football Predictions")

if st.button("Get today's predictions"):
    data = get_worldwide_predictions()
    for item in data:
        st.write(f"{item['home_team']} vs {item['away_team']} ({item['url']})")
        st.json(item["prediction"])
        st.markdown("---")

if st.button("Show performance report"):
    accuracy = calculate_accuracy()
    st.metric(label="Prediction Accuracy", value=f"{accuracy}%")
