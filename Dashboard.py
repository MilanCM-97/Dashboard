from Sentiment_analys import *
from Schedule_post import *
from wordcloud import WordCloud, STOPWORDS
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
import plotly.express as px
import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

# from Social_network_analysis import *

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("Social Media Dashboard")
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>',
    unsafe_allow_html=True
)

# File Uploader
MAX_FILE_SIZE = 209715200
fl = st.file_uploader(
    "Upload a File",
    type=(["csv", "txt", "xlsx", "xls"])
)

# Sample file downloader
with open("sample_data_file.xlsx", "rb") as file:
    btn = st.download_button(
        label="Download the Sample Document",
        data=file,
        file_name="sample.xls"
    )

try:
    if fl is not None:
        st.toast(fl)

    elif fl is not None and len(fl.read()) > MAX_FILE_SIZE:
        st.error("File is too large!")
        st.stop()

    else:
        st.error("Please upload a Data File!")
        st.stop()

    xls = pd.ExcelFile(fl)
    df = pd.read_excel(
        io=xls,
        sheet_name="Data"
    )
    # Create Side Bar
    st.sidebar.image("images/dialog.png", width=100)
    st.markdown(" ")

# Filters
    st.sidebar.header("Please Filter Here")

    platform = st.sidebar.multiselect(
        "Select Platform:",
        options=df["Platform"].unique(),
        default=df["Platform"].unique()
    )

    year = st.sidebar.multiselect(
        "Select the Year:",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )

    month = st.sidebar.multiselect(
        "Select the Month:",
        options=df["Month"].unique(),
        default=df["Month"].unique(),
    )

    df_selection = df.query(
        "Platform == @platform & Year == @year & Month == @month"
    )

# Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  # This will halt the app from further execution.

    st.markdown("""---""")

# KPI's
    st.subheader("Top KPI's")
    total_followers = int(df_selection["Followers"].sum())
    total_reactions = int(df_selection["Reactions"].sum())
    total_comments = int(df_selection["Comments"].sum())
    total_shares = int(df_selection["Shares"].sum())

    column_1, column_2, column_3, column_4 = st.columns(4)

    with column_1:
        st.metric(
            label="Total Followers",
            value=f"{total_followers:,}",
            delta="Number of Followers"
        )

    with column_2:
        st.metric(
            label="Total Reactions",
            value=f"{total_reactions:,}",
            delta="Number of Reactions"
        )

    with column_3:
        st.metric(
            label="Total Comments",
            value=f"{total_comments:,}",
            delta="Number of comments"
        )

    with column_4:
        st.metric(
            label="Total Shares",
            value=f"{total_shares:,}",
            delta="Number of shares"
        )

# style the metric
    style_metric_cards(
        background_color="#EFF0F5",
        border_left_color="#B41076",
        border_color="#E0E0E0",
        box_shadow=False
    )

    st.markdown("""---""")

    column_1, column_2 = st.columns(2)

    with column_1:
        # st.subheader('User Engagement by Platform')
        fig = px.pie(
            df_selection,
            values="User engagement rate",
            names="Platform",
            title="User Engagement by Platform"
        )
        fig.update_traces(
            text=df_selection["Platform"],
            textposition="inside"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with column_2:
        # st.subheader('User Engagement by Device')
        fig = px.histogram(
            df_selection,
            x="Platform",
            y=["Views by Desktop", "Views by Mobile"],
            text_auto='',
            barmode="group",
            title="User Engagement by Device"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.markdown("""---""")

except Exception as e:
    st.error("The format of this data file is not correct. Please download the Sample Document and follow the same format!")
    st.stop()

df = pd.read_excel(
    io=xls,
    sheet_name="Metrics"
)

Sentiment_analys(fl)

st.markdown("""---""")

Schedule_post()
