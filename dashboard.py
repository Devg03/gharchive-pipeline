import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px

# Connection
client = bigquery.Client(project="gharchive-pipeline")

# Page Setup
st.set_page_config(page_title="GH Archive Pipeline", layout="wide")
st.title("GitHub Archive Activity Dashboard")

# Query 1: top repos
@st.cache_data
def load_top_repos():
    query = """
        SELECT repo_name, event_count
        FROM `gharchive-pipeline.gharchive_dbt.mart_top_repos`
        ORDER BY event_count DESC
        LIMIT 20
    """
    return client.query(query).to_dataframe()

top_repos = load_top_repos()

st.header("Top Repositories by Activity")
st.dataframe(top_repos)

st.subheader("Top 20 Repositories")
fig = px.bar (
    top_repos.sort_values("event_count"),
    x="event_count",
    y="repo_name",
    orientation="h",
    title="Top 20 Repositories by Event Count",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# Query 2: events by type
@st.cache_data
def load_events_by_type():
    query = """
        SELECT type, events_by_type
        FROM `gharchive-pipeline.gharchive_dbt.stg_events_by_type`
        ORDER BY events_by_type DESC
    """

    return client.query(query).to_dataframe()

events = load_events_by_type()

st.header("Events by Type")
st.bar_chart(events, x="type", y="events_by_type")