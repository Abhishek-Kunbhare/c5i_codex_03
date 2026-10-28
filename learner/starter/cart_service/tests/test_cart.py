import unittest
from datetime import datetime, timedelta, timezone

from src.cart import calculate_total, calculate_total_with_coupon

class CartContractTests(unittest.TestCase):
    def test_existing_total_contract(self):
        result = calculate_total([{"price": 5, "quantity": 2}, {"price": 3, "quantity": 1}])
        self.assertEqual(result, 13)
        self.assertIsInstance(result, (int, float))

    def test_empty_cart_is_zero(self):
        self.assertEqual(calculate_total([]), 0)


class CouponTests(unittest.TestCase):
    def setUp(self):
        self.active_from = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
        self.expires_at = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
        self.coupon = {
            "code": "SAVE20",
            "active_from": self.active_from,
            "expires_at": self.expires_at,
            "percent": 20,
        }
        self.items = [{"price": 100, "quantity": 1}]

    def total(self, now, code="SAVE20", coupon=None, items=None):
        return calculate_total_with_coupon(
            self.items if items is None else items,
            self.coupon if coupon is None else coupon,
            code,
            now,
        )

    def test_case_insensitive_match_and_mismatch(self):
        self.assertEqual(self.total(self.active_from, code="save20"), 80.0)
        self.assertEqual(self.total(self.active_from, code="OTHER"), 100)

    def test_activation_boundary(self):
        instant = timedelta(microseconds=1)
        self.assertEqual(self.total(self.active_from - instant), 100)
        self.assertEqual(self.total(self.active_from), 80.0)

    def test_expiry_and_grace_boundaries(self):
        instant = timedelta(microseconds=1)
        cutoff = self.expires_at + timedelta(hours=1)
        self.assertEqual(self.total(self.expires_at - instant), 80.0)
        self.assertEqual(self.total(self.expires_at), 80.0)
        self.assertEqual(self.total(self.expires_at + timedelta(minutes=30)), 80.0)
        self.assertEqual(self.total(cutoff - instant), 80.0)
        self.assertEqual(self.total(cutoff), 80.0)
        self.assertEqual(self.total(cutoff + instant), 100)

    def test_percentage_bounds_cap_and_zero_floor(self):
        for percent, expected in [(0, 100.0), (100, 50.0)]:
            with self.subTest(percent=percent):
                self.assertEqual(self.total(self.active_from, coupon={**self.coupon, "percent": percent}), expected)
        self.assertEqual(
            self.total(self.active_from, coupon={**self.coupon, "percent": 100}, items=[{"price": 250, "quantity": 1}]),
            200.0,
        )
        self.assertEqual(
            self.total(self.active_from, coupon={**self.coupon, "percent": 100}, items=[{"price": 10, "quantity": 1}]),
            0.0,
        )
        for percent in (-1, 101, "invalid"):
            with self.subTest(invalid_percent=percent):
                with self.assertRaises(ValueError):
                    self.total(self.active_from, coupon={**self.coupon, "percent": percent})

    def test_rounding_half_up_to_cents(self):
        self.assertEqual(
            self.total(self.active_from, coupon={**self.coupon, "percent": 50}, items=[{"price": 0.01, "quantity": 1}]),
            0.01,
        )

    def test_missing_coupon_or_code_keeps_original_total(self):
        self.assertEqual(calculate_total_with_coupon(self.items, None, "SAVE20", self.active_from), 100)
        self.assertEqual(self.total(self.active_from, code=None), 100)

    def test_timestamp_validation(self):
        naive = datetime(2026, 1, 1, 10)
        non_utc = timezone(timedelta(hours=1))
        with self.assertRaises(ValueError):
            self.total(naive)
        with self.assertRaises(ValueError):
            self.total(self.active_from.astimezone(non_utc))
        with self.assertRaises(ValueError):
            self.total(self.active_from, coupon={**self.coupon, "expires_at": naive})
        with self.assertRaises(ValueError):
            self.total(self.active_from, coupon={**self.coupon, "expires_at": self.active_from - timedelta(seconds=1)})

if __name__ == "__main__":
    unittest.main()
