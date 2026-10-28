from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def calculate_total(items):
    """Return the unadjusted total for item dictionaries with price and quantity."""
    return sum(item["price"] * item["quantity"] for item in items)


def calculate_total_with_coupon(items, coupon, code, now):
    """Return the total after a coupon, including its one-hour UTC grace period.

    A missing coupon or code leaves the total unchanged. Invalid coupon data raises
    an error. Discounted totals are rounded to cents using ROUND_HALF_UP.
    """
    total = calculate_total(items)
    if coupon is None or code is None:
        return total

    if not isinstance(code, str) or not isinstance(coupon["code"], str):
        raise TypeError("coupon codes must be strings")

    active_from = coupon["active_from"]
    expires_at = coupon["expires_at"]
    for value in (active_from, expires_at, now):
        if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
            raise ValueError("coupon timestamps must be timezone-aware UTC datetimes")
    if expires_at < active_from:
        raise ValueError("expires_at must not precede active_from")

    try:
        percent = Decimal(str(coupon["percent"]))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("coupon percent must be between 0 and 100") from exc
    if not percent.is_finite() or not 0 <= percent <= 100:
        raise ValueError("coupon percent must be between 0 and 100")

    if code.casefold() != coupon["code"].casefold():
        return total
    if not active_from <= now <= expires_at + timedelta(hours=1):
        return total

    subtotal = Decimal(str(total))
    discount = min(subtotal * percent / 100, Decimal("50"))
    discounted_total = max(Decimal("0"), subtotal - discount)
    return float(discounted_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
