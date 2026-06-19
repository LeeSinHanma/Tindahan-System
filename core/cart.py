class Cart:
    def __init__(self) -> None:
        self._items: dict[int, dict] = {}
        self._no_profit_pricing = False

    def set_no_profit_pricing(self, enabled: bool) -> None:
        self._no_profit_pricing = bool(enabled)
        for item in self._items.values():
            item["price"] = item["original_price"] if self._no_profit_pricing else item["sell_price"]

    def add_product(self, product: dict) -> bool:
        product_id = product["id"]
        current = self._items.get(product_id)
        sell_price = float(product.get("sell_price", product.get("price", 0)))
        original_price = float(product.get("original_price", sell_price))
        unit_price = original_price if self._no_profit_pricing else sell_price
        stock = int(product.get("stock", 0))
        sellable_stock = int(product.get("sellable_stock", stock))
        stock_tracked = bool(product.get("stock_tracked", False))

        if stock_tracked and sellable_stock <= 0:
            return False

        if current is None:
            self._items[product_id] = {
                "product_id": product_id,
                "name": product["name"],
                "barcode": product["barcode"],
                "price": unit_price,
                "sell_price": sell_price,
                "original_price": original_price,
                "quantity": 1,
                "stock": stock,
                "sellable_stock": sellable_stock,
                "stock_tracked": stock_tracked,
            }
            return True

        if not current.get("stock_tracked", False):
            current["quantity"] += 1
            return True

        available_stock = int(current.get("sellable_stock", current["stock"]))
        if current["quantity"] < available_stock:
            current["quantity"] += 1
            return True

        return False

    def remove_product(self, product_id: int) -> None:
        self._items.pop(product_id, None)

    def update_quantity(self, product_id: int, quantity: int) -> None:
        if product_id not in self._items:
            return
        if quantity <= 0:
            self.remove_product(product_id)
            return

        stock = self._items[product_id]["stock"]
        sellable_stock = int(self._items[product_id].get("sellable_stock", stock))
        if self._items[product_id].get("stock_tracked", False):
            self._items[product_id]["quantity"] = min(quantity, sellable_stock)
        else:
            self._items[product_id]["quantity"] = quantity

    def clear(self) -> None:
        self._items.clear()

    def get_items(self) -> list[dict]:
        items = []
        for item in self._items.values():
            subtotal = item["price"] * item["quantity"]
            items.append({**item, "subtotal": subtotal})
        return items

    def get_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self._items.values())
