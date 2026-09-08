def get_previous_year_month(report_month):
    year, month = report_month.split("-")
    return f"{int(year) - 1}-{month}"
