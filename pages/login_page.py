from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
    
    def clear_error(self) -> None:
        if self.is_visible(self.ERROR_BUTTON):
            self.click(self.ERROR_BUTTON)
