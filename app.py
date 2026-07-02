import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="France Spotify Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------
st.markdown("""
<style>

/* Sidebar Background */
[data-testid="stSidebar"]{
    background-color:#1F2937;
}

/* Change all sidebar text to white */
[data-testid="stSidebar"] *{
    color:white !important;
}

/* Multiselect labels */
[data-testid="stSidebar"] label{
    color:white !important;
    font-weight:bold;
}

/* Slider labels */
[data-testid="stSidebar"] .stSlider label{
    color:white !important;
}

/* Markdown & Titles */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp{
    background-color:#F3F4F6;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.main{
background:#0B1120;
color:white;
}

section[data-testid="stSidebar"]{
background:#111827;
}

h1,h2,h3,h4{
color:white;
}

.kpi{
padding:20px;
border-radius:15px;
color:white;
text-align:center;
font-weight:bold;
box-shadow:0px 5px 15px rgba(0,0,0,0.3);
}

.green{
background:linear-gradient(135deg,#00C853,#64DD17);
}

.blue{
background:linear-gradient(135deg,#2979FF,#00B0FF);
}

.orange{
background:linear-gradient(135deg,#FB8C00,#FFA726);
}

.purple{
background:linear-gradient(135deg,#7B1FA2,#BA68C8);
}

.red{
background:linear-gradient(135deg,#E53935,#EF5350);
}

footer{
visibility:hidden;
}

</style>
""",unsafe_allow_html=True)

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.markdown("""
# 🎵 France Top 50 Spotify Playlist Analytics Dashboard

### Audience Sensitivity • Content Compliance • Format Preference Analysis
""")

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

@st.cache_data
def load_data():

    df=pd.read_csv("Atlantic_France.csv")

    df["date"]=pd.to_datetime(df["date"],dayfirst=True)

    df["duration_min"]=df["duration_ms"]/60000

    return df

df=load_data()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.image(
"https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg",
width=120
)

st.sidebar.title("🎛 Dashboard Filters")

# Artist

artist=st.sidebar.multiselect(

"🎤 Select Artist",

sorted(df["artist"].unique()),

default=[]

)

# Album

album=st.sidebar.multiselect(

"💿 Album Type",

sorted(df["album_type"].unique()),

default=sorted(df["album_type"].unique())

)

# Explicit

explicit=st.sidebar.multiselect(

"🔞 Explicit",

sorted(df["is_explicit"].unique()),

default=sorted(df["is_explicit"].unique())

)

# Popularity

popularity=st.sidebar.slider(

"⭐ Popularity",

int(df["popularity"].min()),

int(df["popularity"].max()),

(

int(df["popularity"].min()),

int(df["popularity"].max())

)

)

# Duration

duration=st.sidebar.slider(

"⏱ Duration (Minutes)",

float(df["duration_min"].min()),

float(df["duration_min"].max()),

(

float(df["duration_min"].min()),

float(df["duration_min"].max())

)

)

# ----------------------------------------------------
# FILTER DATA
# ----------------------------------------------------

if artist:

    df=df[df["artist"].isin(artist)]

df=df[df["album_type"].isin(album)]

df=df[df["is_explicit"].isin(explicit)]

df=df[df["popularity"].between(popularity[0],popularity[1])]

df=df[df["duration_min"].between(duration[0],duration[1])]

# ----------------------------------------------------
# KPI CALCULATIONS
# ----------------------------------------------------

total_songs=len(df)

artists=df["artist"].nunique()

avg_popularity=round(df["popularity"].mean(),2)

avg_duration=round(df["duration_min"].mean(),2)

explicit_percent=round(df["is_explicit"].mean()*100,2)

album_percent=round((df["album_type"]=="album").mean()*100,2)

single_percent=round((df["album_type"]=="single").mean()*100,2)

avg_tracks=round(df["total_tracks"].mean(),2)

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

col1,col2,col3,col4=st.columns(4)

with col1:

    st.markdown(f"""
    <div class='kpi green'>
    <h3>🎵 Songs</h3>
    <h1>{total_songs}</h1>
    </div>
    """,unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class='kpi blue'>
    <h3>🎤 Artists</h3>
    <h1>{artists}</h1>
    </div>
    """,unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class='kpi orange'>
    <h3>⭐ Avg Popularity</h3>
    <h1>{avg_popularity}</h1>
    </div>
    """,unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class='kpi purple'>
    <h3>⏱ Avg Duration</h3>
    <h1>{avg_duration}</h1>
    </div>
    """,unsafe_allow_html=True)

col5,col6,col7,col8=st.columns(4)

with col5:

    st.markdown(f"""
    <div class='kpi red'>
    <h3>🔞 Explicit %</h3>
    <h1>{explicit_percent}%</h1>
    </div>
    """,unsafe_allow_html=True)

with col6:

    st.markdown(f"""
    <div class='kpi green'>
    <h3>💿 Album %</h3>
    <h1>{album_percent}%</h1>
    </div>
    """,unsafe_allow_html=True)

with col7:

    st.markdown(f"""
    <div class='kpi blue'>
    <h3>🎧 Single %</h3>
    <h1>{single_percent}%</h1>
    </div>
    """,unsafe_allow_html=True)

with col8:

    st.markdown(f"""
    <div class='kpi orange'>
    <h3>📀 Avg Album Size</h3>
    <h1>{avg_tracks}</h1>
    </div>
    """,unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# INTERACTIVE CHARTS
# ==========================================================

st.header("📊 Playlist Analytics")

# ----------------------------------------------------------
# ROW 1
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        df,
        names="is_explicit",
        hole=0.55,
        color="is_explicit",
        color_discrete_sequence=["#EF4444", "#10B981"],
        title="🎵 Explicit vs Clean Songs"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

with col2:

    album_count = (
        df["album_type"]
        .value_counts()
        .reset_index()
    )

    album_count.columns = ["Album Type", "Count"]

    fig = px.pie(
        album_count,
        names="Album Type",
        values="Count",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="💿 Album Type Distribution"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# ROW 2
# ----------------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    top_artist = (
        df["artist"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_artist.columns = ["Artist", "Songs"]

    fig = px.bar(
        top_artist,
        x="Songs",
        y="Artist",
        orientation="h",
        color="Songs",
        color_continuous_scale="Turbo",
        title="🎤 Top 10 Artists"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

with col4:

    top_song = (
        df.sort_values(
            "popularity",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_song,
        x="song",
        y="popularity",
        color="artist",
        title="🏆 Top 10 Most Popular Songs"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# ROW 3
# ----------------------------------------------------------

col5, col6 = st.columns(2)

with col5:

    fig = px.histogram(
        df,
        x="duration_min",
        nbins=30,
        color_discrete_sequence=["#00E5FF"],
        title="⏱ Song Duration Distribution"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

with col6:

    fig = px.scatter(
        df,
        x="duration_min",
        y="popularity",
        color="album_type",
        hover_name="song",
        size="total_tracks",
        title="📈 Duration vs Popularity"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# ROW 4
# ----------------------------------------------------------

col7, col8 = st.columns(2)

with col7:

    fig = px.box(
        df,
        x="album_type",
        y="popularity",
        color="album_type",
        title="🔥 Popularity by Album Type"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

with col8:

    fig = px.scatter(
        df,
        x="total_tracks",
        y="popularity",
        color="album_type",
        hover_name="song",
        title="📀 Album Size vs Popularity"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# ROW 5
# ----------------------------------------------------------

st.subheader("🌡 Correlation Heatmap")

corr = df.select_dtypes(include="number").corr()

heat = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="Turbo",
        text=corr.round(2).values,
        texttemplate="%{text}",
        hoverongaps=False
    )
)

heat.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    heat,
    use_container_width=True
)

# ----------------------------------------------------------
# ROW 6
# ----------------------------------------------------------

st.subheader("⭐ Popularity Distribution")

fig = px.histogram(
    df,
    x="popularity",
    color="album_type",
    marginal="box",
    nbins=30,
    title="Popularity Score Distribution"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# ROW 7
# ----------------------------------------------------------

st.subheader("🎼 Playlist Ranking")

top50 = df.sort_values("position").head(50)

fig = px.line(
    top50,
    x="position",
    y="popularity",
    markers=True,
    color="album_type",
    hover_name="song",
    title="Position vs Popularity"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# ROW 8
# ----------------------------------------------------------

st.subheader("🎧 Explicit Songs by Album Type")

explicit_chart = (
    df.groupby(["album_type", "is_explicit"])
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    explicit_chart,
    x="album_type",
    y="Count",
    color="is_explicit",
    barmode="group",
    title="Explicit Songs Across Album Types"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("## 📌 Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### 🎵 Playlist Summary

- Total Songs : **{len(df)}**
- Unique Artists : **{df['artist'].nunique()}**
- Average Popularity : **{round(df['popularity'].mean(),2)}**
- Average Duration : **{round(df['duration_min'].mean(),2)} Minutes**
- Average Album Size : **{round(df['total_tracks'].mean(),2)} Tracks**
""")

with col2:

    explicit = round(df["is_explicit"].mean()*100,2)

    album = round((df["album_type"]=="album").mean()*100,2)

    single = round((df["album_type"]=="single").mean()*100,2)

    st.info(f"""
### 📊 Content Analysis

🔞 Explicit Songs : **{explicit}%**

💿 Album Tracks : **{album}%**

🎧 Single Tracks : **{single}%**
""")


# ============================================================
# TOP SONG TABLE
# ============================================================

st.markdown("## 🏆 Top 10 Songs")

top_song_table = df.sort_values(
    "popularity",
    ascending=False
)[[
    "song",
    "artist",
    "popularity",
    "album_type",
    "duration_min"
]].head(10)

st.dataframe(
    top_song_table,
    use_container_width=True
)

# ============================================================
# TOP ARTIST TABLE
# ============================================================

st.markdown("## 🎤 Top Artists")

artist_table = (
    df.groupby("artist")
    .agg(
        Songs=("song","count"),
        AvgPopularity=("popularity","mean")
    )
    .sort_values(
        "Songs",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    artist_table,
    use_container_width=True
)

# ============================================================
# DATA PREVIEW
# ============================================================

st.markdown("## 📄 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ============================================================
# DOWNLOAD BUTTON
# ============================================================

st.markdown("## 📥 Download Filtered Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

label="📥 Download CSV",

data=csv,

file_name="France_Top50_Filtered.csv",

mime="text/csv"

)

# ============================================================
# DASHBOARD SUMMARY
# ============================================================

st.markdown("## 📈 Dashboard Summary")

col1,col2,col3=st.columns(3)

with col1:

    st.metric(
        "Highest Popularity",
        df["popularity"].max()
    )

with col2:

    st.metric(
        "Lowest Popularity",
        df["popularity"].min()
    )

with col3:

    st.metric(
        "Longest Song (Minutes)",
        round(df["duration_min"].max(),2)
    )

# ============================================================
# ABOUT PROJECT
# ============================================================

st.markdown("---")

st.markdown("""
# 📚 About Project

This dashboard analyzes **France Top 50 Spotify Playlist**
to understand audience listening behaviour.

### Objectives

✔ Audience Sensitivity Analysis

✔ Explicit Content Analysis

✔ Album vs Single Analysis

✔ Song Duration Analysis

✔ Popularity Analysis

✔ Artist Performance Analysis

✔ Album Structure Analysis

✔ Business Insights

""")

# ============================================================
# TECHNOLOGIES
# ============================================================

st.markdown("""
### 🛠 Technologies Used

- Python

- Pandas

- NumPy

- Plotly

- Streamlit

- Data Analytics

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center'>

<h2>🎵 France Spotify Analytics Dashboard</h2>

<p>Developed by <b>Aastha Sapate</b></p>

<p>MIT-WPU | MCA | Data Analytics Portfolio Project</p>

<p>Made with ❤️ using Streamlit & Plotly</p>

</div>
""",
unsafe_allow_html=True
)