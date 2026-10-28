def calculate_total(items):
    """Return the unadjusted total for item dictionaries with price and quantity."""
    return sum(item["price"] * item["quantity"] for item in items)
