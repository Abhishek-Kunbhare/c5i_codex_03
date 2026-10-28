import unittest
from src.notifications import send_order_confirmation

class FakeSender:
    def __init__(self):
        self.orders = []
    def send(self, order):
        self.orders.append(order)
        return "sent"

class NotificationContractTests(unittest.TestCase):
    def test_existing_sender_interface(self):
        sender = FakeSender()
        result = send_order_confirmation(sender, {"id": "O-1"})
        self.assertEqual(result, "sent")
        self.assertEqual(sender.orders, [{"id": "O-1"}])

if __name__ == "__main__":
    unittest.main()
