import streamlit as st
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

sales_all = st.session_state.get("sales_all")

if sales_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen.")
else:
    periods = sorted(sales_all['Berichtsmonat'].unique())
    col_a, col_b = st.columns(2)

    with col_a:
        selected_period = st.selectbox("Periode", periods, index=len(periods) - 1)

    with col_b:
        comparison_options = ["Kein Vergleich"] + periods
        selected_comparison = st.selectbox("Vergleichen mit", comparison_options)

#Filter data for selected period
    current_df = sales_all[ sales_all["Berichtsmonat"] == selected_period]

     # KPI calculation
    revenue = total_revenue(current_df)
    units = total_units(current_df)
    product_name, product_revenue = top_product(current_df)

    # when no comparison
    revenue_delta = None
    units_delta = None
    comparison_product_name = None

    #Calculate comparison only if selected
    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_all[sales_all["Berichtsmonat"]== selected_comparison]

        st.write("Vergleich ausgewählt:", selected_comparison)
        st.write("Comparison shape:", comparison_df.shape)

        comparison_revenue = total_revenue(comparison_df)
        comparison_units = total_units(comparison_df)
        comparison_product_name, _ = top_product(comparison_df)

        revenue_delta = calculate_change(revenue, comparison_revenue)
        units_delta = calculate_change(units, comparison_units)

    #KPI'S

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Gesamtumsatz", f"{revenue:,.2f} €", delta=f"{revenue_delta:.1f} %" if revenue_delta is not None else None)

    with col2:
        st.metric("Verkaufte Stückzahl", f"{units:,.0f}", delta=f"{units_delta:.1f} %" if units_delta is not None else None)

    with col3:
        st.metric("Bestseller", product_name)
        st.caption(f"Umsatz: {product_revenue:,.2f} €")

        if comparison_product_name:
            st.caption(f"Vergleich: {comparison_product_name}")
