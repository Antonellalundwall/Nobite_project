import streamlit as st
import plotly.express as px
import pandas as pd

from src.kpis import (
    calculate_endbestand,
    calculate_lagerabgang,
    calculate_lagerreichweite,
    calculate_lagerstatus,
    calculate_change
)

st.set_page_config(page_title="Lager & Planung", page_icon="📈", layout="wide")
st.title("📈 Lager & Nachfrage")
st.divider()

# get the inventory data uploaded
inventory_all = st.session_state.get("inventory_all")

if inventory_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen. ⚠️")
else:
    periods = sorted(inventory_all["Berichtsmonat"].unique())

    col_a, col_b = st.columns(2)

    selected_period = col_a.selectbox("Periode", periods, index=len(periods) - 1)
    selected_comparison = col_b.selectbox("Vergleichen mit", ["Kein Vergleich"] + periods)

    current_df = inventory_all[inventory_all["Berichtsmonat"] == selected_period]

    # KPI calculations
    endbestand = calculate_endbestand(current_df)
    lagerabgang = calculate_lagerabgang(current_df)
    lagerreichweite = calculate_lagerreichweite(current_df)
    lagerstatus = calculate_lagerstatus(current_df)

    # when no comparison
    endbestand_delta = None
    lagerabgang_delta = None
    lagerreichweite_delta = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = inventory_all[inventory_all["Berichtsmonat"] == selected_comparison]

        comparison_endbestand = calculate_endbestand(comparison_df)
        comparison_lagerabgang = calculate_lagerabgang(comparison_df)
        comparison_lagerreichweite = calculate_lagerreichweite(comparison_df)

        endbestand_delta = calculate_change(endbestand, comparison_endbestand)
        lagerabgang_delta = calculate_change(lagerabgang, comparison_lagerabgang)
        lagerreichweite_delta = calculate_change(lagerreichweite, comparison_lagerreichweite)

    # KPI blocks
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Endbestand", f"{endbestand:,.0f} Stück", delta=f"{endbestand_delta:.1f} %" if endbestand_delta is not None else None, border=True)
    col2.metric("Lagerabgang", f"{lagerabgang:,.0f} Stück", delta=f"{lagerabgang_delta:.1f} %" if lagerabgang_delta is not None else None, border=True)
    col3.metric("Lagerreichweite", f"{lagerreichweite:.1f} Monate", delta=f"{lagerreichweite_delta:.1f} %" if lagerreichweite_delta is not None else None, border=True)
    col4.metric("Lagerstatus", lagerstatus, border=True)

    ################################### Charts ###################################

    # Stock Overview
    st.subheader("Lagerbestand nach Produkt")

    stock_by_product = current_df.groupby("Bezeichnung", as_index=False)["Endbestand"].sum()

    fig = px.bar(
        stock_by_product,
        x="Endbestand",
        y="Bezeichnung",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)
