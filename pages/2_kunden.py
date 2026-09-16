import streamlit as st
import plotly.express as px
import json
import pandas as pd

from src.kpis import (
    top_customer,
    top_region,
    top_customer_share,
    calculate_change
)

st.set_page_config(page_title="Kunden & Regionale Performance in Deutschland", page_icon="📈", layout="wide")
st.title("📈 Kunden & Regionale Performance")
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
    customer_name, customer_revenue = top_customer(current_df)
    region_name, region_revenue = top_region(current_df)
    customer_share = top_customer_share(current_df)

 # when no comparison
    share_delta = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_view[
            sales_view["Anzeigeperiode"] == selected_comparison]

        comparison_share = top_customer_share(comparison_df)
        share_delta = calculate_change(
            customer_share,
            comparison_share
        )

#KPI blocks
    col4, col5, col6 = st.columns(3)

    col4.metric("Top-Großhändler", customer_name, border=True)

    col5.metric("Top-Region", region_name, border=True)

    col6.metric("Umsatzanteil Top-Großhändler", f"{customer_share:.1f} %", delta=f"{share_delta:.1f} %" if share_delta is not None else None, border=True)
    st.divider()
################################### Charts: #############################################
    col7, col8 = st.columns(2)

#Top Customers by Revenue bar chart
    col7.subheader("Die 5 Umsatzstärksten Großhändler")

    top_customers = (current_df.groupby("Kundengrupp", as_index=False)["Umsatz"].sum()
    .sort_values("Umsatz", ascending=False)
    .head(5)
    )

    fig = px.bar(
        top_customers,
        x="Umsatz",
        y="Kundengrupp",
        orientation="h"
    )
    col7.plotly_chart(fig, use_container_width=True)

# Revenue Concentration pie chart
    col8.subheader("Umsatzanteile der 5 umsatzstärksten Großhändler")
    revenue_by_top_customers = (current_df.groupby("Kundengrupp", as_index=False)["Umsatz"].sum().sort_values("Umsatz", ascending=False).head(5))

    fig = px.pie(revenue_by_top_customers, values="Umsatz", names="Kundengrupp", hole=0.4)
    col8.plotly_chart(fig, use_container_width=True)
    st.divider()

############# Regional Performance map:
#performance matrix

    with open("data/reference/germany_states.geojson", "r", encoding="utf-8") as file:
        germany_states = json.load(file)

    regional_data = (current_df.groupby("Bundesland").agg({"Liefermenge": "sum", "Umsatz": "sum"}).reset_index())

    regional_data = regional_data.sort_values("Umsatz", ascending=False)
    regional_data.index = range(1, len(regional_data) + 1)


# Germany Map:
    st.subheader("Regional Performance")

    #map/top region/ selected region
    map_col, top_col, detail_col = st.columns([1.4, 0.8, 1.2])

#map
    fig = px.choropleth_map(
        regional_data,
        geojson=germany_states,
        locations="Bundesland",
        featureidkey="properties.shapeName",
        color="Umsatz",
        color_continuous_scale=[
            "#dbeafe",
            "#93c5fd",
            "#3b82f6",
            "#1d4ed8"],
        hover_name="Bundesland",
        hover_data={
        "Umsatz": ":,.2f",
        "Liefermenge": ":,.0f",
        "Bundesland": False},

        center={"lat": 51.1657, "lon": 10.4515},
        zoom = 5.0,
        map_style="white-bg",
        height=550
    )

    fig.update_traces(marker_line_color="#666666", marker_line_width=1.2)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    map_col.plotly_chart(fig, use_container_width=True)

# top regions
    top_regions = regional_data.head(3)

    with top_col:
        st.markdown("### Top Regionen")
        for i, row in enumerate(top_regions.itertuples(), start=1):
            st.write(f"**{i}. {row.Bundesland}**")
            st.caption(f"{row.Umsatz:,.2f} €")


# selected region
    with detail_col:
        selected_region_name = st.selectbox("Region auswählen", regional_data["Bundesland"])
        selected_region = regional_data[regional_data["Bundesland"] == selected_region_name].iloc[0]

        with st.container(border=True):
            st.markdown(f"### {selected_region_name}")
            st.metric("Umsatz", f"{selected_region['Umsatz']:,.2f} €")
            st.metric("Verkaufte Stückzahl", f"{selected_region['Liefermenge']:,.0f}")
    st.divider()
################################# KEY INSIGHTS #################################
    st.subheader("Key Insights")

    insights = []
    # Total revenue
    total_revenue = current_df["Umsatz"].sum()

    # Top wholesaler
    insights.append(
        f"🏆 **Top-Großhändler:** {customer_name} erzielt "
        f"**{customer_revenue:,.2f} € Umsatz** und macht "
        f"**{customer_share:.1f} % des Gesamtumsatzes** aus.")

    # Top 5 customer concentration
    top_5_revenue = top_customers["Umsatz"].sum()
    top_5_share = (top_5_revenue / total_revenue) * 100

    insights.append(
        f"📊 **Kundenkonzentration:** Die fünf umsatzstärksten Großhändler "
        f"machen zusammen **{top_5_share:.1f} % des Gesamtumsatzes** aus."
    )
    # Strongest region
    region_share = (region_revenue / total_revenue) * 100

    insights.append(
        f"📍 **Top-Region:** {region_name} ist mit "
        f"**{region_revenue:,.2f} € Umsatz** die stärkste Region "
        f"und macht **{region_share:.1f} % des Gesamtumsatzes** aus."
    )

    # Comparison
    if share_delta is not None:

        if share_delta > 0:
            insights.append(
                f"⬆️ **Top-Großhändler Anteil:** Der Umsatzanteil des "
                f"umsatzstärksten Großhändlers ist im Vergleich zur ausgewählten "
                f"Periode um **{share_delta:.1f} % gestiegen**."
            )

        elif share_delta < 0:
            insights.append(
                f"⬇️ **Top-Großhändler Anteil:** Der Umsatzanteil des "
                f"umsatzstärksten Großhändlers ist im Vergleich zur ausgewählten "
                f"Periode um **{abs(share_delta):.1f} % gesunken**."
            )

        else:
            insights.append(
                "➡️ **Top-Großhändler Anteil:** Der Umsatzanteil des "
                "umsatzstärksten Großhändlers ist im Vergleich zur ausgewählten "
                "Periode unverändert."
            )

#all insights in one box:
    st.info("\n\n".join(insights))
