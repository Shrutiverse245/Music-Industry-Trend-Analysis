import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ---- Load the dataset ----
file_path = "MusicData.csv"
df = pd.read_csv(file_path)

# ---- Convert necessary columns to numeric ----
numeric_cols = ["Views", "Likes", "Comments", "Stream"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert and handle errors

# ---- Streamlit Page Configuration ----
st.set_page_config(
    page_title="Music Industry Trends",
    page_icon="🎶",
    layout="wide"
)

# ---- Title & Introduction ----
st.title("🎵 Music Industry Trends")
st.write("Explore insights on popular music based on YouTube views, likes, comments, and streaming data.")

# ---- Sidebar: Filters for User Interaction ----
st.sidebar.header("🎤 Filter Options")

# Artist Selection Dropdown
artist_list = ["All"] + sorted(df["Artist"].unique().tolist())
selected_artist = st.sidebar.selectbox("🎼 Select an Artist", artist_list)

# Apply Artist Filter
if selected_artist != "All":
    df = df[df["Artist"] == selected_artist]

# Search Bar for Tracks & Albums
search_query = st.sidebar.text_input("🔍 Search Track or Album")

# Apply Search Filter
if search_query:
    df = df[
        df["Track"].str.contains(search_query, case=False, na=False) | 
        df["Album"].str.contains(search_query, case=False, na=False)
    ]

# ---- Display Music Data Table ----
st.subheader("🎶 Music Data Table")
st.dataframe(
    df[["Artist", "Track", "Album", "Views", "Likes", "Comments", "Stream"]],
    height=300
)

# ---- Visualization: Top 10 Artists by Streams (Bar Chart) ----
st.subheader("🌟 Top 10 Artists by Streams")

top_artists = df.groupby("Artist")["Stream"].sum().sort_values(ascending=False).head(10)

fig1 = px.bar(
    top_artists, 
    x=top_artists.index, 
    y=top_artists.values, 
    labels={"y": "Total Streams"}, 
    title="Top 10 Artists by Streams",
    color=top_artists.values, 
    color_continuous_scale="rainbow"
)
st.plotly_chart(fig1, use_container_width=True)

# ---- Visualization: Most Viewed Songs on YouTube (Bar Chart) ----
st.subheader("📺 Most Viewed Songs on YouTube")

top_songs = df.sort_values(by="Views", ascending=False).head(10)

fig2 = px.bar(
    top_songs, 
    x="Track", 
    y="Views", 
    hover_data=["Artist"], 
    title="Top 10 Most Viewed Songs", 
    color="Views", 
    color_continuous_scale="sunset"
)
st.plotly_chart(fig2, use_container_width=True)

# ---- Visualization: Streams Percentage (Pie Chart) ----
st.subheader("🍰 Streams Distribution by Artist")

pie_data = df.groupby("Artist")["Stream"].sum().nlargest(5)  # Top 5 Artists
fig3 = px.pie(
    pie_data, 
    names=pie_data.index, 
    values=pie_data.values, 
    title="Top 5 Artists by Stream Percentage",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig3)

# ---- Visualization: Trend Over Time (Line Chart) ----
st.subheader("📈 Music Popularity Over Time")

# Simulate a 'Date' column if it's missing
if "Release Date" not in df.columns:
    np.random.seed(42)
    df["Release Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")

# Aggregate by date
df_time = df.groupby("Release Date")[["Views", "Likes", "Stream"]].sum()

# Create Line Chart
fig4, ax = plt.subplots(figsize=(10, 5))
df_time.plot(kind="line", ax=ax, marker="o", linestyle="-")
ax.set_title("Trends in Views, Likes, and Streams Over Time")
ax.set_ylabel("Count")
st.pyplot(fig4)

# ---- Visualization: Seaborn Bar Chart for Views ----
st.subheader("📊 Views Comparison Between Top 10 Artists")

fig5, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_artists.index, 
    y=top_artists.values, 
    palette="coolwarm", 
    ax=ax
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_title("Views Comparison of Top 10 Artists")
ax.set_ylabel("Total Views")
st.pyplot(fig5)

# ---- Correlation Heatmap ----
st.subheader("📊 Correlation Between Music Features")

correlation_matrix = df[["Views", "Likes", "Comments", "Stream", "Danceability", "Energy", "Tempo"]].corr()

fig6, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
st.pyplot(fig6)

# ---- Summary Statistics ----
st.subheader("📈 Statistical Summary of Numeric Data")
st.write(df.describe())

# ---- Footer ----
st.write("🎶 Enjoy exploring the music industry!")