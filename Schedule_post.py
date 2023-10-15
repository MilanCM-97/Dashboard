import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Create schedule post

def Schedule_post():
    st.header("Post Schedular")
    st.write("By scheduling posts in advance, you can strategically align your content with special events, holidays, or marketing campaigns. This ensures your content is timely and relevant.")

    st.markdown(
        '<style>div.block-container{padding-top:1rem;}</style>',
        unsafe_allow_html=True
    )

    with st.form("post_schedule"):
        column_1, column_2 = st.columns(2)

        with column_1:
            date = st.date_input("Select Date")

        with column_2:
            time = st.time_input("Select Time")

        title = st.text_input("Post title")
        description = st.text_area("Descripetion")

        fl = st.file_uploader(
            "Upload a File",
            type=(["jpg", "jpeg", "png", "mp4", "pdf"])
        )

        st.form_submit_button('Schedule post')
