import unittest
from src.cart import calculate_total

class CartContractTests(unittest.TestCase):
    def test_existing_total_contract(self):
        result = calculate_total([{"price": 5, "quantity": 2}, {"price": 3, "quantity": 1}])
        self.assertEqual(result, 13)
        self.assertIsInstance(result, (int, float))

    def test_empty_cart_is_zero(self):
        self.assertEqual(calculate_total([]), 0)

if __name__ == "__main__":
    unittest.main()
