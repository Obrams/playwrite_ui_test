from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List


class CartPage(BasePage):
    
    CART_ITEMS = ".cart_item"
    CART_ITEM_NAMES = ".inventory_item_name"
    CART_ITEM_PRICES = ".inventory_item_price"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"
    REMOVE_BUTTONS = "[id^='remove-']"
    CART_QUANTITY = ".cart_quantity"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_cart_items_count(self) -> int:
        return self.get_element_count(self.CART_ITEMS)
    
    def get_cart_item_names(self) -> List[str]:
        return self.get_all_text_contents(self.CART_ITEM_NAMES)
    
    def get_cart_item_prices(self) -> List[float]:
        price_texts = self.get_all_text_contents(self.CART_ITEM_PRICES)
        return [float(price.replace("$", "")) for price in price_texts]
    
    def remove_item(self, product_name: str) -> None:
        product_id = product_name.lower().replace(" ", "-")
        remove_button = f"[data-test='remove-{product_id}']"
        self.click(remove_button)
    
    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BUTTON)
    
    def is_cart_empty(self) -> bool:
        return self.get_cart_items_count() == 0
