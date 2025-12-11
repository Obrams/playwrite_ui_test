from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    
    PRODUCT_ITEMS = ".inventory_item"
    PRODUCT_NAMES = ".inventory_item_name"
    PRODUCT_PRICES = ".inventory_item_price"
    ADD_TO_CART_BUTTONS = ".btn_inventory"
    cart_badge = ".shopping_cart_badge"
    cart_link = ".shopping_cart_link"
    SORT_DROPDOWN = ".product_sort_container"
    burger_menu = "#react-burger-menu-btn"
    logout_link = "#logout_sidebar_link"
    
    def __init__(self, page):
        super().__init__(page)
    
    def get_products_count(self):
        return self.get_element_count(self.PRODUCT_ITEMS)
    
    def add_product_to_cart(self, product_name):
        product_id = product_name.lower().replace(" ", "-")
        self.click(f"[data-test='add-to-cart-{product_id}']")
    
    def remove_product_from_cart(self, product_name):
        product_id = product_name.lower().replace(" ", "-")
        self.click(f"[data-test='remove-{product_id}']")
    
    def get_cart_badge_count(self):
        if self.is_visible(self.cart_badge):
            return self.get_text(self.cart_badge)
        return 0
    
    def is_cart_badge_visible(self):
        return self.is_visible(self.cart_badge)
    
    def go_to_cart(self):
        self.click(self.cart_link)
    
    def sort_products(self, option):
        self.select_option(self.SORT_DROPDOWN, option)
    
    def get_product_names(self):
        return self.get_all_text_contents(self.PRODUCT_NAMES)
    
    def get_product_prices(self):
        prices = self.get_all_text_contents(self.PRODUCT_PRICES)
        return [float(p.replace("$", "")) for p in prices]
    
    def logout(self):
        self.click(self.burger_menu)
        self.wait_for_element(self.logout_link)
        self.click(self.logout_link)
