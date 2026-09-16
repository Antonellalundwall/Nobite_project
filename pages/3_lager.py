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

def format_reichweite(monate):
    ganze_monate = int(monate)
    tage = round((monate - ganze_monate) * 30)

    if ganze_monate == 0:
        return f"ca. {tage} Tage"

    elif ganze_monate == 1:
        return f"ca. 1 Monat & {tage} Tage"

    else:
        return f"ca. {ganze_monate} Monate & {tage} Tage"

st.set_page_config(page_title="Lager & Planung", page_icon="📈", layout="wide")
st.title("📈 Lager & Nachfrage")
st.divider()

# get the inventory data uploaded
inventory_all = st.session_state.get("inventory_all")

if inventory_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen. ⚠️")
else:
     # Copy data for period selection
    inventory_view = inventory_all.copy()

 # Choose view: month; half year, full year
    ansicht = st.radio(
        "Ansicht",
        ["Monat", "Halbjahr", "Jahr"],
        horizontal=True
    )
#month
    if ansicht == "Monat":
        inventory_view["Anzeigeperiode"] = inventory_view["Berichtsmonat"]

#half year
    elif ansicht == "Halbjahr":
        jahr = inventory_view["Berichtsmonat"].str[:4]
        monat = inventory_view["Berichtsmonat"].str[5:7].astype(int)
        halbjahr = monat.apply(
            lambda m: "H1" if m <= 6 else "H2")
        inventory_view["Anzeigeperiode"] = jahr + "-" + halbjahr

#year
    else:
        inventory_view["Anzeigeperiode"] = inventory_view["Berichtsmonat"].str[:4]

    # Available periods
    periods = sorted(inventory_view["Anzeigeperiode"].unique())


    col_a, col_b = st.columns(2)
    selected_period = col_a.selectbox("Periode", periods, index=len(periods) - 1)
    selected_comparison = col_b.selectbox("Vergleichen mit", ["Kein Vergleich"] + periods)

    # Filter selected period
    current_df = inventory_view[
    inventory_view["Anzeigeperiode"] == selected_period]

    # Last available month in selected period
    latest_month = current_df["Berichtsmonat"].max()
    current_stock_df = current_df[current_df["Berichtsmonat"] == latest_month]


    # KPI calculations
    endbestand = calculate_endbestand(current_stock_df)
    lagerabgang = calculate_lagerabgang(current_df)
    lagerreichweite = calculate_lagerreichweite(current_stock_df)
    lagerstatus = calculate_lagerstatus(current_stock_df)

    # when no comparison
    endbestand_delta = None
    lagerabgang_delta = None
    lagerreichweite_delta = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = inventory_view[
            inventory_view["Anzeigeperiode"] == selected_comparison]

        comparison_latest_month = comparison_df["Berichtsmonat"].max()

        comparison_stock_df = comparison_df[
            comparison_df["Berichtsmonat"] == comparison_latest_month]

        comparison_endbestand = calculate_endbestand(comparison_stock_df)
        comparison_lagerabgang = calculate_lagerabgang(comparison_df)
        comparison_lagerreichweite = calculate_lagerreichweite(comparison_stock_df)

        endbestand_delta = calculate_change(
            endbestand,
            comparison_endbestand
        )

        lagerabgang_delta = calculate_change(
            lagerabgang,
            comparison_lagerabgang
        )

        lagerreichweite_delta = calculate_change(
            lagerreichweite,
            comparison_lagerreichweite
        )

    # KPI blocks
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Endbestand (Periodenende)", f"{endbestand:,.0f} Stück", delta=f"{endbestand_delta:.1f} %" if endbestand_delta is not None else None, border=True)
    col2.metric("Lagerabgang", f"{lagerabgang:,.0f} Stück", delta=f"{lagerabgang_delta:.1f} %" if lagerabgang_delta is not None else None, border=True)
    reichweite_text = f"{lagerreichweite:.1f}".replace(".", ",")
    col3.metric("Lagerreichweite (Periodenende)", format_reichweite(lagerreichweite), delta=f"{lagerreichweite_delta:.1f} %" if lagerreichweite_delta is not None else None, border=True)
    col4.metric("Lagerstatus (Periodenende)", lagerstatus, border=True)
    st.divider()
    ################################### Charts ###################################

    # Stock Overview
    st.subheader("Lagerbestand nach Produkt")

    stock_by_product = current_stock_df.groupby("Bezeichnung", as_index=False)["Endbestand"].sum()

    fig = px.bar(
        stock_by_product,
        x="Endbestand",
        y="Bezeichnung",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    #Lagerabgang trend over time
    st.subheader("Lagerabgang nach Monaten")
    monthly_outflow = (inventory_all.groupby("Berichtsmonat", as_index=False)["Abgang"].sum().sort_values("Berichtsmonat"))

    monatsnamen = {
    "01": "Jan", "02": "Feb", "03": "Mär", "04": "Apr",
    "05": "Mai", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Okt", "11": "Nov", "12": "Dez"
}
    monthly_outflow["Abgang"] = monthly_outflow["Abgang"].abs()

    monthly_outflow["Monat"] = (monthly_outflow["Berichtsmonat"].str[5:7].map(monatsnamen))

    monthly_outflow["Jahr"] = (monthly_outflow["Berichtsmonat"].str[2:4])

    monthly_outflow["Label"] = (monthly_outflow["Monat"] + " " + monthly_outflow["Jahr"])

    monthly_outflow["Abgang (k)"] = (monthly_outflow["Abgang"] / 1000).round(0).astype(int).astype(str) + "k"

    table_view = monthly_outflow.set_index("Label")[["Abgang (k)"]].T
    st.dataframe(table_view, use_container_width=True)
    st.divider()
#Matrix
    st.subheader("Lagerbestand & Lagerabgang nach Produkt")

    # Endbestand pro Produkt
    stock_by_product = (current_stock_df.groupby("Bezeichnung", as_index=False)["Endbestand"].sum())

    # Lagerabgang pro Produkt
    outflow_by_product = (current_df.groupby("Bezeichnung", as_index=False)["Abgang"].sum())

    outflow_by_product["Abgang"] = outflow_by_product["Abgang"].abs()

    # Beide Tabellen zusammenführen
    product_inventory = pd.merge(stock_by_product, outflow_by_product, on="Bezeichnung")

    product_inventory = product_inventory.rename(columns={
    "Bezeichnung": "Produkt",
    "Abgang": "Lagerabgang"})

    st.dataframe(product_inventory,  use_container_width=True, hide_index=True)
    st.divider()

################################# KEY INSIGHTS #################################

    st.subheader("Key Insights")

    insights = []

    # Highest stock
    highest_stock = product_inventory.loc[product_inventory["Endbestand"].idxmax()]

    # Top wholesaler
    insights.append(
        f"🏆 **Höchster Lagerbestand:** {highest_stock['Produkt']} "
        f"hat am Periodenende mit **{highest_stock['Endbestand']:,.0f} Stück** "
        f"den höchsten Bestand.")

    # lowest stock
    lowest_stock = product_inventory.loc[product_inventory["Endbestand"].idxmin()]

    insights.append(
        f"⚠️ **Niedrigster Lagerbestand:** {lowest_stock['Produkt']} "
        f"hat am Periodenende mit **{lowest_stock['Endbestand']:,.0f} Stück** "
    )
    # highest outflow
    highest_outflow = product_inventory.loc[product_inventory["Lagerabgang"].idxmax()]

    insights.append(
        f"📦 **Höchster Lagerabgang:** {highest_outflow['Produkt']} "
        f"hat im ausgewählten Zeitraum mit **{highest_outflow['Lagerabgang']:,.0f} Stück** "
        f"den höchsten Lagerabgang."
    )

    #all insights in one box:
    st.info("\n\n".join(insights))
