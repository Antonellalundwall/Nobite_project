# KPI functions for Nobite Analytics
import pandas as pd

def calculate_change(current_value, comparison_value):
    # Calculate percentage change between two periods
    if comparison_value == 0:
        return None

    return (
        (current_value - comparison_value)
        / comparison_value
        * 100
    )

# Dashboard 1: Sales & Product Performance

def total_revenue(df):
    # KPI 1: Total Revenue
    return df['Umsatz'].sum()


def total_units(df):
    # KPI 2: Units Sold
    return df['Liefermenge'].sum()


def top_product(df):
    # KPI 3: Top Product by Revenue
    product_revenue = (
        df.groupby('Bezeichnung')['Umsatz']
        .sum()
        .sort_values(ascending=False)
    )

    return product_revenue.index[0], product_revenue.iloc[0]

# Product Performance Matrix
def product_performance(current_df, comparison_df=None):

    # Current Product Performance
    product_performance = (
        current_df.groupby("Bezeichnung")
        .agg(
            Umsatz=("Umsatz", "sum"),
            Verkaufte_Stückzahl=("Liefermenge", "sum")
        )
        .reset_index()
    )

    # No Comparison
    if comparison_df is None:
        return product_performance

    # Comparison Product Performance
    comparison_performance = (
        comparison_df.groupby("Bezeichnung")
        .agg(
            Umsatz_Vergleich=("Umsatz", "sum"),
            Stückzahl_Vergleich=("Liefermenge", "sum")
        )
        .reset_index()
    )

    # Merge Product Performance
    merged_df = pd.merge(
        product_performance,
        comparison_performance,
        on="Bezeichnung"
    )

    # Revenue Change
    merged_df["Umsatzveränderung"] = (
        (merged_df["Umsatz"] - merged_df["Umsatz_Vergleich"])
        / merged_df["Umsatz_Vergleich"]
    ) * 100

    # Units Change
    merged_df["Stückzahlveränderung"] = (
        (merged_df["Verkaufte_Stückzahl"] - merged_df["Stückzahl_Vergleich"])
        / merged_df["Stückzahl_Vergleich"]
    ) * 100

    return merged_df

## Sales Trend Line Chart
def sales_trend(sales_all):

    # Revenue per Month
    trend_df = (
        sales_all
        .groupby("Berichtsmonat", as_index=False)["Umsatz"]
        .sum()
    )

    # Split Year and Month
    trend_df["Jahr"] = trend_df["Berichtsmonat"].str[:4]
    trend_df["Monat"] = trend_df["Berichtsmonat"].str[5:7]

    # Prepare Year Comparison
    year_comparison = trend_df.pivot(
        index="Monat",
        columns="Jahr",
        values="Umsatz"
    ).reset_index()

    return year_comparison

# Dashboard 2: Customer & Regional Performance

def top_customer(df):
    # KPI 1: Top Customer by Revenue
    customer_revenue = (
        df.groupby('Kundengrupp')['Umsatz']
        .sum()
        .sort_values(ascending=False)
    )

    return customer_revenue.index[0], customer_revenue.iloc[0]


def top_region(df):
    # KPI 2: Top Region by Revenue
    region_revenue = (
        df.groupby('Bundesland')['Umsatz']
        .sum()
        .sort_values(ascending=False)
    )

    return region_revenue.index[0], region_revenue.iloc[0]


def top_customer_share(df):
    # KPI 3: Top Customer Share
    customer_revenue = (
        df.groupby('Kundengrupp')['Umsatz']
        .sum()
        .sort_values(ascending=False)
    )

    top_customer_revenue = customer_revenue.iloc[0]
    total_revenue_value = df['Umsatz'].sum()

    return (
        top_customer_revenue
        / total_revenue_value
        * 100
    )


def revenue_change_yoy(current_df, previous_year_df):
    # KPI 4: Revenue Change vs same month last year
    current_revenue = total_revenue(current_df)
    previous_year_revenue = total_revenue(previous_year_df)

    return calculate_change(
        current_revenue,
        previous_year_revenue
    )

# Dashboard 3: Inventory & Demand


def calculate_endbestand(inventory):
    return inventory["Endbestand"].sum()


def calculate_lagerabgang(inventory):
    return abs(inventory["Abgang"].sum())


def calculate_lagerreichweite(inventory):
    endbestand = calculate_endbestand(inventory)
    lagerabgang = calculate_lagerabgang(inventory)

    if lagerabgang == 0:
        return 0

    return round(endbestand / lagerabgang, 1)


def calculate_lagerstatus(inventory):
    lagerreichweite = calculate_lagerreichweite(inventory)

    if lagerreichweite >= 3:
        return "Ausreichend"
    elif lagerreichweite >= 2:
        return "Beobachten"
    else:
        return "Niedrig"
