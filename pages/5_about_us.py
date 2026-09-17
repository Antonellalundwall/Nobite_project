import streamlit as st
from src.navigation import show_navigation

st.set_page_config(page_title="About Us", page_icon="🦟", layout="wide")
show_navigation()
st.title("🦟 About Us")
st.divider()

st.image(
    "images/about_us.png",
    use_container_width=True
)

st.subheader("Über NOBITE")
st.write("NOBITE ist eine Marke der Tropical Concept SARL mit Sitz in Paris, Frankreich. "
    "Das Unternehmen ist auf Insekten- und Tropenschutz spezialisiert und vertreibt "
    "seine Produkte unter anderem in Deutschland, Österreich und der Schweiz.")

st.subheader("Unser Schutzkonzept")
st.write(
    "Das NOBITE Schutzkonzept kombiniert zwei Maßnahmen: "
    "ein langanhaltendes Repellent für die Haut und ein Imprägnierungsmittel "
    "für Kleidung. Gemeinsam bieten sie einen umfassenden Schutz vor Mücken "
    "und anderen Arthropoden.")

st.subheader("Für Reisen & Alltag")
st.write(
    "NOBITE ist besonders für Reisen in tropische Regionen konzipiert, "
    "in denen durch Mücken übertragene Krankheiten wie Malaria, Dengue-Fieber "
    "oder Zika vorkommen können. Die Produkte können aber auch zum Schutz "
    "vor Mücken und Zecken in Europa eingesetzt werden.")
