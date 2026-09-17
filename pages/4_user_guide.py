import streamlit as st
from src.navigation import show_navigation

st.set_page_config(page_title="User Guide", page_icon="👤", layout="wide")
show_navigation()
st.title("📘 User Guide")
st.divider()

st.subheader("So funktioniert die Website")
st.write("In wenigen Schritten von den monatlichen Reports"
         " zu den wichtigsten Business insights.")
st.divider()

st.subheader("1. Datein hochladen")
st.write("Auf der Startseite die gewünschten Umsatzstatistikem und Lagerlisten"
         "per Drag & Drop hochladen. Es können mehrer Monate gleichzeitig"
         "hochgeladen werden.")

st.subheader("2. Analyse auswählen")
st.write("Danach eine der drei Analysen öffnen: Umsatz & Produktperformance,"
         " Kunden & Regionale Performemnce oder Lager & Nachfrage")

st.subheader("3. Zeitraum auswählen")
st.write("Über Ansicht kann man zwischen Monat, Halbjahr und Jahr wechseln"
         " und anschließend die gewünschte periode aussuchen.")

st.subheader("4. Vergleich auswählen")
st.write("Zusätzlich kann eine Vergleichsperiode ausgewählt werden,"
         " um Veränderungen zwischen den Perioden direkt zu sehen.")

st.subheader("5. Ergebnisse analysieren")
st.write("Die wichtigsten KPI'S, Charts und Key Insights geben einen schnellen"
         " Überblick über die Geschäftsentwicklungen.")

st.subheader("6. Zwischen Analysen wechseln")
st.write("Über die Navigation auf der linken Seite können jeder Zeit die anderen"
         "Bereiche geöffnet werden und die hochgeladenen Daten bleiben während"
         "der Session verfügbar.")

st.subheader("7. Analyse neu starten")
st.write("Wenn man mit der Analyse fertig ist, einfach zu der Startseite"
         " zurückkehren und bei Bedarf mit neuen Datein eine Analyse starten.")
