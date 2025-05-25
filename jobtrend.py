import streamlit as st
import pandas as pd
from scraper.rozee_scraper import scrape_rozee_jobs
import os

st.title("Real-Time Job Trend Analyzer")

# User input for keyword
keyword = st.text_input("Enter job keyword", "data analyst")

# Button to run scraper
if st.button("Scrape Jobs"):
    with st.spinner("Scraping jobs from Rozee.pk..."):
        jobs = scrape_rozee_jobs(keyword)
    st.success(f"Scraped {len(jobs)} jobs!")
else:
    # Load existing data if available
    csv_path = "data/jobs.csv"
    if os.path.exists(csv_path):
        jobs = pd.read_csv(csv_path)
    else:
        jobs = pd.DataFrame()

if jobs.empty:
    st.warning("No job data available. Please scrape jobs first.")
else:
    # If jobs is a list of dicts (from scraping), convert to DataFrame
    if isinstance(jobs, list):
        jobs = pd.DataFrame(jobs)

    st.subheader("Top 5 Job Titles")
    top_titles = jobs['Title'].value_counts().head(5)
    st.bar_chart(top_titles)

    st.subheader("Top Skills Required")
    # skills are comma-separated strings, split and count frequencies
    all_skills = jobs['Skills'].dropna().str.cat(sep=', ').lower().split(', ')
    skills_series = pd.Series(all_skills).value_counts().head(10)
    st.bar_chart(skills_series)

    st.subheader("Top Hiring Cities")
    top_cities = jobs['Location'].value_counts().head(5)
    st.bar_chart(top_cities)

    st.subheader("Job Posting Trends Over Time")
    if 'Date' in jobs.columns:
        try:
            jobs['Date'] = pd.to_datetime(jobs['Date'], errors='coerce')
            trend = jobs['Date'].dt.date.value_counts().sort_index()
            st.line_chart(trend)
        except Exception as e:
            st.write("Error parsing dates:", e)
    else:
        st.write("Date info not available to show trends.")