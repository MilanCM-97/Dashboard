from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import plotly.express as px
import streamlit as st
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')


def Sentiment_analys(fl):
    # Polrity of the comments
    st.subheader('General polrity of the comments')

    st.markdown(
        '<style>div.block-container{padding-top:1rem;}</style>',
        unsafe_allow_html=True
    )

    xls = pd.ExcelFile(fl)
    df = pd.read_excel(
        io=xls,
        engine="openpyxl",
        sheet_name="Comments"
    )

    # Finding polarity for each comment
    polarity = []
    for i in df["Comments"]:
        try:
            polarity. append(TextBlob(i).sentiment.polarity)
        except:
            polarity. appendend(0)

    df["Polarity"] = polarity

    positive_polarity = df[df['Polarity'] == 0.1]
    negative_polarity = df[df['Polarity'] == -0]

    total_negative_comments = " ".join(negative_polarity["Comments"])
    total_positive_comments = " ".join(positive_polarity["Comments"])

    # Overall polarity of the comments
    comments = str(df["Comments"])
    polarity = TextBlob(comments).polarity
    subjectivity = TextBlob(comments).subjectivity

    column_1, column_2 = st.columns(2)
    try:
        with column_1:
            if (polarity < 0):
                st.metric(
                    label="Overall Polarity of the Comments",
                    value="Negative Impression",
                )
            else:
                st.metric(
                    label="Overall  Polarity of the Comments",
                    value="Positive",
                )

        with column_2:
            if (subjectivity < 0):
                st.metric(
                    label="More About the Comments",
                    value="Comments are Objective",
                )
            else:
                st.metric(
                    label="More About the Comments",
                    value="Comments are Subjective",
                )
    except Exception as e:
        if positive_polarity.empty:
            st.warning("No Positive Comments to Show!")

    st.markdown(" ")
    column_1, column_2 = st.columns(2)

    # Create popular Wordcloud
    with column_1:
        try:
            wordcloud = WordCloud(
                stopwords=set(STOPWORDS),
                background_color="rgba(255, 255, 255, 0)",
                width=500,
                mode="RGBA").generate(total_positive_comments)

            fig3 = px.imshow(
                wordcloud,
                title="Popular Words",
            )

            fig3.update_xaxes(showgrid=False, showticklabels=False)
            fig3.update_yaxes(showgrid=False, showticklabels=False)

            st.plotly_chart(
                fig3,
                use_container_width=True
            )
        except Exception as e:
            st.error("Oops! Something went wrong")

    with column_2:
        df = df.groupby(["Language"])[
            "Language"].count().reset_index(name="count")
        fig2 = px.pie(
            df,
            values="count",
            names="Language",
            title="Comments by Language Types",
            hole=.4
        )
        fig2.update_traces(
            text=df["Language"],
            textposition="inside"
        )
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.subheader("URLs of the Negative Comments")
    st.markdown(" ")
    st.dataframe(
        negative_polarity,
        height=400,
        use_container_width=True,
        column_order=("Polarity", "URL", "Date")
    )
