import pandas as pd


# Inventory data cleaning
def clean_text(text):
    return str(text).replace('¸', 'ü').replace('ˆ', 'ö')


# Sales data cleaning
def clean_sales(df, plz_df):
    df = df.copy()

    # Clean IDs and codes
    df['PLZ'] = df['PLZ'].astype(str).str.zfill(5)
    df['BestellNr.'] = df['BestellNr.'].astype(str)
    df['Artikel'] = df['Artikel'].astype(str)
    df['PZN'] = df['PZN'].astype(str)

    # Clean text
    df['Ort'] = df['Ort'].apply(clean_text)
    df['Bezeichnung'] = df['Bezeichnung'].apply(clean_text)

    # Clean revenue values
    df['Umsatz'] = df['Umsatz'].apply(
        lambda x: x.replace(',', '.') if isinstance(x, str) else x
    )

    df['Umsatz'] = pd.to_numeric(
        df['Umsatz'],
        errors='coerce'
    )

    # Free deliveries generate no revenue
    free_delivery_mask = (
        df['Umsatz'].isna()
        & df['Auftragsart'].eq('Kostenlose Lieferung')
    )

    df.loc[free_delivery_mask, 'Umsatz'] = 0

    # Clean date
    df['Versanddatum'] = pd.to_datetime(
        df['Versanddatum'],
        dayfirst=True,
        errors='coerce'
    )

    # Create reporting month
    df['Berichtsmonat'] = (
        df['Versanddatum']
        .dt.to_period('M')
        .astype(str)
    )

    # Add regional information
    df = df.merge(
        plz_df,
        on='PLZ',
        how='left'
    )

    return df
