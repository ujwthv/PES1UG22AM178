import json
from cart import dao
from products import Product, get_product_by_id  # Import individual product fetch

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list[Product]:
    """Fetch the cart details for a user."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    items = []
    for cart_detail in cart_details:
        try:
            # Safely parse contents using json.loads
            contents = json.loads(cart_detail['contents'])
            items.extend(contents)
        except json.JSONDecodeError:
            continue  # Skip invalid entries
    
    # Fetch product details one by one (inefficient but individual)
    product_details = [get_product_by_id(product_id) for product_id in items]
    return product_details


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
