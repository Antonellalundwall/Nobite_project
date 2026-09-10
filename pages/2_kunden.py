import streamlit as st
import plotly.express as px
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
    periods = sorted(sales_all["Berichtsmonat"].unique())

    col_a, col_b = st.columns(2)

    selected_period = col_a.selectbox("Periode", periods, index=len(periods) - 1)

    selected_comparison = col_b.selectbox("Vergleichen mit", ["Kein Vergleich"] + periods)


#filter selected period
    current_df = sales_all[sales_all["Berichtsmonat"] == selected_period]



 # KPI calc
    customer_name, customer_revenue = top_customer(current_df)
    region_name, region_revenue = top_region(current_df)
    customer_share = top_customer_share(current_df)

 # when no comparison
    share_delta = None

    if selected_comparison != "Kein Vergleich":
        comparison_df = sales_all[sales_all["Berichtsmonat"] == selected_comparison]
        comparison_share = top_customer_share(comparison_df)
        share_delta = calculate_change(customer_share, comparison_share)

#KPI blocks
    col4, col5, col6 = st.columns(3)

    col4.metric("Top-Großhändler", customer_name, border=True)

    col5.metric("Top-Region", region_name, border=True)

    col6.metric("Umsatzanteil Top-Großhändler", f"{customer_share:.1f} %", delta=f"{share_delta:.1f} %" if share_delta is not None else None, border=True)

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
