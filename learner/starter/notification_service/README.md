# Notification service starter

The existing `send_order_confirmation(sender, order)` interface calls the injected sender once. Tests use a fake sender. Run with `python3 -m unittest discover -s tests -v`. The starter never contacts a real provider.
