from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    
    SUCCESS_HEADER = ".complete-header"
    SUCCESS_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "#back-to-products"
    PONY_EXPRESS_IMAGE = ".pony_express"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def is_order_complete(self) -> bool:
        return self.is_visible(self.SUCCESS_HEADER) and \
               self.is_visible(self.PONY_EXPRESS_IMAGE)
    
    def get_success_header(self) -> str:
        return self.get_text(self.SUCCESS_HEADER)
    
    def get_success_text(self) -> str:
        return self.get_text(self.SUCCESS_TEXT)
    
    def back_to_products(self) -> None:
        self.click(self.BACK_HOME_BUTTON)
