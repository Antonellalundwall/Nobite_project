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
