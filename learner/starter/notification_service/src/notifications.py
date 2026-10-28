def send_order_confirmation(sender, order):
    """Send a confirmation through the injected sender and return its result."""
    return sender.send(order)
