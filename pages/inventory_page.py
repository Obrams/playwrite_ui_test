from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import List


class InventoryPage(BasePage):
    
    PRODUCT_ITEMS = ".inventory_item"
    PRODUCT_NAMES = ".inventory_item_name"
    PRODUCT_PRICES = ".inventory_item_price"
    ADD_TO_CART_BUTTONS = ".btn_inventory"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = ".product_sort_container"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def get_products_count(self) -> int:
        return self.get_element_count(self.PRODUCT_ITEMS)
    
    def add_product_to_cart(self, product_name: str) -> None:
        product_id = product_name.lower().replace(" ", "-")
        add_button = f"[data-test='add-to-cart-{product_id}']"
        self.click(add_button)
    
    def remove_product_from_cart(self, product_name: str) -> None:
        product_id = product_name.lower().replace(" ", "-")
        remove_button = f"[data-test='remove-{product_id}']"
        self.click(remove_button)
    
    def get_cart_badge_count(self) -> str:
        if self.is_visible(self.SHOPPING_CART_BADGE):
            return self.get_text(self.SHOPPING_CART_BADGE)
        return "0"
    
    def is_cart_badge_visible(self) -> bool:
        return self.is_visible(self.SHOPPING_CART_BADGE)
    
    def go_to_cart(self) -> None:
        self.click(self.SHOPPING_CART_LINK)
    
    def sort_products(self, option: str) -> None:
        self.select_option(self.SORT_DROPDOWN, option)
    
    def get_product_names(self) -> List[str]:
        return self.get_all_text_contents(self.PRODUCT_NAMES)
    
    def get_product_prices(self) -> List[float]:
        price_texts = self.get_all_text_contents(self.PRODUCT_PRICES)
        return [float(price.replace("$", "")) for price in price_texts]
    
    def logout(self) -> None:
        self.click(self.BURGER_MENU)
        self.wait_for_element(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
