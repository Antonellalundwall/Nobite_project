import streamlit as st

st.set_page_config(
    page_title="Nobite Analytics",
    page_icon="🦟",
    layout="wide"
)

st.title("🦟 Nobite Analytics")
st.write("Upload your reports and turn them into insights.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.header("Umsatzstatistik & PLZ")
    sales_files = st.file_uploader("Sales Files hochladen", type=["xlsx"], accept_multiple_files=True)

with col2:
    st.header("Lagerliste")
    inventory_files = st.file_uploader("Inventory files hochladen", type=["xlsx"], accept_multiple_files=True)

if sales_files and inventory_files:

    col3, col4 = st.columns(2)
    with col3: st.success("Data Ready ✅ ")
        st.caption(f"{len(sales_files)} Umsatzstatistiken ausgewählt")
    with col4: st.success("Data Validation ✅ ")
        st.caption(f"{len(inventory_files)} Lagerlisten ausgewählt")

st.header("📊 Choose your analysis")
col5, col6, col7 = st.columns(3)
with col5:
    st.subheader("Umsatz & Produktperformance")
        st.caption("Umsatz | Produkte | Trends         ➜")
if st.button("Analyse öffnen ➜", key="sales"):
    st.switch_page("pages/1_umsatz.py")

with col6:
    st.subheader("Kunden & Regionale Performance")
        st.caption("Kunden | Regionen | Verteilung         ➜")
if st.button("Analyse öffnen ➜", key="customers"):
        st.switch_page("pages/2_kunden.py")


with col7:
    st.subheader("Lager & Nachfrage")
            st.caption("Bestand | Nachfrage | Trends/Planung         ➜")
     if st.button("Analyse öffnen ➜", key="inventory"):
        st.switch_page("pages/3_lager.py")
