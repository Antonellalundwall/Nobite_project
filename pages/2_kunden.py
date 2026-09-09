import streamlit as st
import pandas as pd

from src.kpis import (
    top_customer,
    top_region,
    top_customer_share,
    calculate_change
)

st.set_page_config(page_title="Kunden & Regionale Performance", page_icon="📈", layout="wide")
st.title("📈 Kunden & Regionale Performance")
st.divider()

sales_all = st.session_state.get("sales_all")

if sales_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen.")
else:
    periods = sorted(sales_all["Berichtsmonat"].unique())
    col_a, col_b = st.columns(2)

    with col_a:
        selected_period = st.selectbox("Periode", periods, index=len(periods) - 1)

    with col_b:
        comparison_options = ["Kein Vergleich"] +periods
        selected_comparison = st.selectbox("Vergleichen mit", comparison_options)

    #Filter data for selected period
    current_df = sales_all[ sales_all["Berichtsmonat"] == selected_period]

 # KPI
    customer_name, customer_revenue = top_customer(current_df)
    region_name, region_revenue = top_region(current_df)
    customer_share = top_customer_share(current_df)

 # when no comparison
    share_delta = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_all[sales_all["Berichtsmonat"] == selected_comparison]
        comparison_share = top_customer_share(comparison_df)
        share_delta = calculate_change(customer_share, comparison_share)

#KPIS
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Top Großhändler",customer_name)
        st.caption(f"Umsatz: {customer_revenue:,.2f} €")

    with col5:
        st.metric("Top Region", region_name)
        st.caption(f"Umsatz:{region_revenue:,.2f} €")

    with col6:
        st.metric("Umsatzanteil Top-Großhändler", f"{customer_share:,.1f} %", delta=f"{share_delta:.1f} %" if share_delta is not None else None)
