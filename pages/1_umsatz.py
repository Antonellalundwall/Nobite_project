import streamlit as st
import plotly.express as px
import pandas as pd

from src.kpis import (
    total_revenue,
    total_units,
    top_product,
    calculate_change,
    product_performance,
    sales_trend
)

st.set_page_config(page_title="Umsatz & Produktperformance", page_icon="📈", layout="wide")
st.title("📈 Umsatz & Produktperformance")
st.divider()

# get the sales data uploaded
sales_all = st.session_state.get("sales_all")

if sales_all is None:
    st.warning("Bitte zuerst auf der Startseite Dateien hochladen. ⚠️")
else:
    # Copy data for period selection
    sales_view = sales_all.copy()

    # Choose view: month; half year, full year
    ansicht = st.radio(
        "Ansicht",
        ["Monat", "Halbjahr", "Jahr"],
        horizontal=True
    )
    #month
    if ansicht == "Monat":
        sales_view["Anzeigeperiode"] = sales_view["Berichtsmonat"]

    #half year
    elif ansicht == "Halbjahr":
        jahr = sales_view["Berichtsmonat"].str[:4]
        monat = sales_view["Berichtsmonat"].str[5:7].astype(int)
        halbjahr = monat.apply(
            lambda m: "H1" if m <= 6 else "H2")
        sales_view["Anzeigeperiode"] = jahr + "-" + halbjahr

    #year
    else:
        sales_view["Anzeigeperiode"] = sales_view["Berichtsmonat"].str[:4]

    # Available periods
    periods = sorted(sales_view["Anzeigeperiode"].unique())

    col_a, col_b = st.columns(2)
    selected_period = col_a.selectbox("Periode", periods, index=len(periods) - 1)
    selected_comparison = col_b.selectbox("Vergleichen mit", ["Kein Vergleich"] + periods)

     # Filter selected period
    current_df = sales_view[
    sales_view["Anzeigeperiode"] == selected_period]

    # KPI calc
    revenue = total_revenue(current_df)
    units = total_units(current_df)
    product_name, product_revenue = top_product(current_df)

    # when no comparison
    revenue_delta = None
    units_delta = None
    comparison_product_name = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_view[
            sales_view["Anzeigeperiode"] == selected_comparison]

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

     # Product Performance Matrix
    st.subheader("Allg. Produktperformance Übersicht")

    if selected_comparison != "Kein Vergleich":
        product_table = product_performance(current_df, comparison_df)

        # Only show relevant columns
        product_table = product_table[[
            "Bezeichnung",
            "Umsatz",
            "Verkaufte_Stückzahl",
            "Umsatzveränderung",
            "Stückzahlveränderung"
        ]].copy()

        # Format percentage changes with arrows
        def arrow_format(val):
            if val > 0:
                return f"🟢 ↑ {val:.1f} %"
            elif val < 0:
                return f"🔴 ↓ {abs(val):.1f} %"
            else:
                return f"{val:.1f} %"

        product_table["Umsatzveränderung"] = (
            product_table["Umsatzveränderung"].apply(arrow_format)
        )

        product_table["Stückzahlveränderung"] = (
            product_table["Stückzahlveränderung"].apply(arrow_format)
        )

    else:
        product_table = product_performance(current_df)

    # Rename columns for dashboard
    product_table = product_table.rename(columns={
        "Bezeichnung": "Produkt",
        "Verkaufte_Stückzahl": "Verkaufte Stückzahl"
    })

    # Show table
    st.dataframe(
        product_table,
        use_container_width=True,
        hide_index=True
    )

    ######### Linechart sales years

    st.subheader("Umsatzvergleich nach Jahr")

    trend_table = sales_trend(sales_all)

    st.line_chart(
        trend_table,
        x="Monat"
    )
    ################################# KEY INSIGHTS / AUTOMATED TEXT ########################################

    st.subheader("Key Insights")

    insights = []
    if revenue_delta is not None:

        if revenue_delta > 0:
            insights.append(f"⬆️ **Gesamtumsatz:** Der Gesamtumsatz ist im Vergleich zur ausgewählten Periode um **{revenue_delta:.1f} % gestiegen**.")

        elif revenue_delta < 0:
            insights.append(f"⬇️ **Gesamtumsatz:** Der Gesamtumsatz ist im Vergleich zur ausgewählten Periode um **{abs(revenue_delta):.1f} % gesunken**.")

        else:
            insights.append("➡️ **Gesamtumsatz:** Der Gesamtumsatz ist im Vergleich zur ausgewählten Periode unverändert.")

#Units sold :
    if units_delta is not None:

        if units_delta > 0:
            insights.append(f"📦 **Verkaufte Stückzahl:** Es wurden im Vergleich zur ausgewählten Periode **{units_delta:.1f} % mehr Stück verkauft**.")

        elif units_delta < 0:
            insights.append(f"📦 **Verkaufte Stückzahl:** Es wurden im Vergleich zur ausgewählten Periode **{abs(units_delta):.1f} % weniger Stück verkauft**.")

        else:
            insights.append("📦 **Verkaufte Stückzahl:** Es wurden genauso viele Stück verkauft wie in der Vergleichsperiode.")

#Bestseller:
    bestseller_share = (product_revenue / revenue) * 100
    insights.append(f"🏆 **Bestseller:** {product_name} erzielt **{product_revenue:,.2f} € Umsatz** "
        f"und macht **{bestseller_share:.1f} % des Gesamtumsatzes** aus.")

#Revenue concentration
    top_2_revenue = revenue_by_product.nlargest(2, "Umsatz")["Umsatz"].sum()
    top_2_share = (top_2_revenue / revenue) * 100

    insights.append(
    f"📊 **Top-Produkte Anteil:** Die zwei umsatzstärksten Produkte machen zusammen "
    f"**{top_2_share:.1f} % des Gesamtumsatzes** aus."
)

# Strongest growth and biggest decline:

    if selected_comparison != "Kein Vergleich":

        growth_table = product_performance(current_df, comparison_df)

        strongest_growth = growth_table.loc[growth_table["Umsatzveränderung"].idxmax()]

        biggest_decline = growth_table.loc[growth_table["Umsatzveränderung"].idxmin()]

        if strongest_growth["Umsatzveränderung"] > 0:
            insights.append(
                f"🚀 **Stärkstes Wachstum:** {strongest_growth['Bezeichnung']} "
                f"hat mit **+{strongest_growth['Umsatzveränderung']:.1f} %** "
                f"das stärkste Umsatzwachstum.")

        if biggest_decline["Umsatzveränderung"] < 0:
            insights.append(
                f"⚠️ **Größter Rückgang:** {biggest_decline['Bezeichnung']} "
                f"verzeichnet mit **{biggest_decline['Umsatzveränderung']:.1f} %** "
                f"den größten Umsatzrückgang.")

#all insights in one box:
    st.info("\n\n".join(insights))
