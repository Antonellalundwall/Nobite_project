import streamlit as st
import plotly.express as px
import pandas as pd

from src.kpis import (
    total_revenue,
    total_units,
    top_product,
    calculate_change
)

st.set_page_config(page_title="Umsatz & Produktperformance", page_icon="📈", layout="wide")
st.title("📈 Umsatz & Produktperformance")
st.divider()

# get the sales data uploaded
sales_all = st.session_state.get("sales_all")

if sales_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen. ⚠️")
else:
    periods = sorted(sales_all["Berichtsmonat"].unique())

    col_a, col_b = st.columns(2)

    selected_period = col_a.selectbox("Periode", periods, index=len(periods) - 1)

    selected_comparison = col_b.selectbox("Vergleichen mit", ["Kein Vergleich"] + periods)

    # filter selected period
    current_df = sales_all[sales_all["Berichtsmonat"] == selected_period]

    # KPI calc
    revenue = total_revenue(current_df)
    units = total_units(current_df)
    product_name, product_revenue = top_product(current_df)

    # when no comparison
    revenue_delta = None
    units_delta = None
    comparison_product_name = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_all[sales_all["Berichtsmonat"] == selected_comparison]
        comparison_revenue = total_revenue(comparison_df)
        comparison_units = total_units(comparison_df)
        comparison_product_name, _ = top_product(comparison_df)

        revenue_delta = calculate_change(revenue, comparison_revenue)
        units_delta = calculate_change(units, comparison_units)

    # KPI blocks
    col1, col2, col3 = st.columns(3)

    col1.metric("Gesamtumsatz", f"{revenue:,.2f} €", delta=f"{revenue_delta:.1f} %" if revenue_delta is not None else None, border=True)

    col2.metric("Verkaufte Stückzahl", f"{units:,.0f}", delta=f"{units_delta:.1f} %" if units_delta is not None else None, border=True)

    col3.metric("Bestseller", product_name, border=True)
    st.caption(f"Umsatz: {product_revenue:,.2f} €")

    if comparison_product_name:
        st.caption(f"Vergleich: {comparison_product_name}")


################################### Charts: #############################################
    col4, col5 = st.columns(2)
# Revenue Share by Product :
    col4.subheader("Umsatzanteil nach Produkt")
    revenue_by_product = current_df.groupby("Bezeichnung", as_index=False)["Umsatz"].sum()
    fig = px.pie(revenue_by_product, values="Umsatz", names="Bezeichnung", hole=0.4)
    col4.plotly_chart(fig, use_container_width=True)

# Units Sold by Product
    col5.subheader("Verkaufte Stückzahl nach Produkt")
    units_by_product = current_df.groupby("Bezeichnung", as_index=False)["Liefermenge"].sum()

    fig = px.bar(
        units_by_product,
        x="Liefermenge",
        y="Bezeichnung",
        orientation="h"
    )
    col5.plotly_chart(fig, use_container_width=True)
