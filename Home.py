import streamlit as st
import requests
from datetime import datetime
import streamlit_lottie as lto # type: ignore

st.set_page_config(
    page_title="Chatbot App",
    page_icon=":globe_with_meridians:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

# ---------Load Assets------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl("https://lottie.host/5b073eca-e11c-4391-8593-b28f39ce0870/q0fz2A3kuN.json")

def main():
    with st.container():
        st.title("Chatbots Demo Website")
        st.subheader("Hi, I am Audrius :wave:")
        st.write("I am passionate about finding ways to use and explore the chatbots.")

def header():
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2, gap="small")
        with left_column:
            st.subheader("What this Site for?")
            st.write(
                """
                On this site I am creating small chatbots projects to show possibilities they gives in practical\
                usage of  machine learning models.
                """
            )
        with right_column:
            lto.st_lottie(lottie_coding, height=300, key="coding")  # type: ignore

def footer_section() -> None:
    """
    Render Streamlit Page footer section with Streamlit Title and Write Methods
    :return: None
    """
    with st.container():
        st.write("---")
        year = datetime.now().year
        st.write(f"© {year} audrbar. All rights reserved.")


if __name__ == "__main__":
    main()
    header()
    footer_section()
