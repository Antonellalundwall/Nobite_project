import streamlit as st

st.set_page_config(
    page_title="Nobite Analytics",
    page_icon="🦟",
    layout="wide"
)

st.title("🦟 Nobite Analytics")
st.write("Upload your reports and turn them into insights.")
st.divider()
st.header("Dateien hochladen")
uploaded_files = st.file_uploader("Sales & Inventory Files", type=["xlsx", "xls", "xlsm"], accept_multiple_files=True, label_visibility="collapsed")
umsatzstatistik_list = []
lagerliste = []
# List per file type


col1, col2 = st.columns(2)
with col1:
    st.header("Umsatzstatistik")
    #uploaded_files = st.file_uploader("Sales Files hochladen", type=["xlsx", "xls", "xlsm"], accept_multiple_files=True)
    st.write("### Uploaded Files:")
    if uploaded_files:
        # Loop through every file in the list
        for uploaded_file in uploaded_files:
            if uploaded_file.name.startswith('Umsatzstatistik'):
                # Display each individual name
                st.write(f"- {uploaded_file.name}")
                umsatzstatistik_list.append(uploaded_file)
        st.success("Data Ready ✅")
        st.caption(f"{len(umsatzstatistik_list)} Umsatzstatistiken ausgewählt")

with col2:
    st.header("Lagerliste")
    #inventory_files = st.file_uploader("Inventory files hochladen", type=["xlsx", "xls", "xlsm"], accept_multiple_files=True)
    st.write("### Uploaded Files:")
    if uploaded_files:
        # Loop through every file in the list
        for uploaded_file in uploaded_files:
            if uploaded_file.name.startswith('Lagerliste'):
                # Display each individual name
                st.write(f"- {uploaded_file.name}")
                lagerliste.append(uploaded_file)
        st.success("Data Ready ✅")
        st.caption(f"{len(lagerliste)} Lagerlisten ausgewählt")

if len(lagerliste) != len(umsatzstatistik_list):
    st.warning('Achtung ungleiche Menge an Datein ⚠️ !!! ')

st.divider()
st.header("📊 Choose your Analysis")

col5, col6, col7 = st.columns(3)

with col5:
    st.subheader("Umsatz & Produktperformance")
    st.caption("Umsatz | Produkte | Trends")
    st.write("")

    if st.button("Analyse öffnen ➜", key="sales"):
        st.switch_page("pages/1_umsatz.py")

with col6:
    st.subheader("Kunden & Regionale Performance")
    st.caption("Kunden | Regionen | Verteilung")
    st.write("")

    if st.button("Analyse öffnen ➜", key="customers"):
        st.switch_page("pages/2_kunden.py")


with col7:
    st.subheader("Lager & Nachfrage")
    st.caption("Bestand | Nachfrage | Trends/Planung")
    st.write("")

    if st.button("Analyse öffnen ➜", key="inventory"):
        st.switch_page("pages/3_lager.py")
