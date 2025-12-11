from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import Dict


class CheckoutPage(BasePage):
    
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "#cancel"
    ERROR_MESSAGE = "[data-test='error']"
    
    CART_ITEMS = ".cart_item"
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
    SUBTOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "#finish"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
    
    def click_continue(self) -> None:
        self.click(self.CONTINUE_BUTTON)
    
    def click_cancel(self) -> None:
        self.click(self.CANCEL_BUTTON)
    
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
    
    def get_order_summary(self) -> Dict[str, float]:
        subtotal_text = self.get_text(self.SUBTOTAL)
        tax_text = self.get_text(self.TAX)
        total_text = self.get_text(self.TOTAL)
        
        subtotal = float(subtotal_text.split("$")[1])
        tax = float(tax_text.split("$")[1])
        total = float(total_text.split("$")[1])
        
        return {
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }
    
    def get_items_count(self) -> int:
        return self.get_element_count(self.CART_ITEMS)
    
    def finish_checkout(self) -> None:
        self.click(self.FINISH_BUTTON)
