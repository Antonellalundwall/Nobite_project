# KPI functions for Nobite Analytics


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
