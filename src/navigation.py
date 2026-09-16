import streamlit as st

def show_navigation():

    with st.sidebar:

        st.page_link("app.py", label="app")

        st.divider()

        st.page_link("pages/1_umsatz.py", label="umsatz")
        st.page_link("pages/2_kunden.py", label="kunden")
        st.page_link("pages/3_lager.py", label="lager")

        st.divider()

        st.page_link("pages/4_user_guide.py", label="user guide")
        st.page_link("pages/5_about_us.py", label="about us")
