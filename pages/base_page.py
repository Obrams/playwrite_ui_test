from playwright.sync_api import Page
from typing import Optional


class BasePage:
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str) -> None:
        self.page.goto(url)
    
    def click(self, selector: str) -> None:
        self.page.click(selector)
    
    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)
    
    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()
    
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
    
    def wait_for_element(self, selector: str, timeout: int = 10000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def get_element_count(self, selector: str) -> int:
        return self.page.locator(selector).count()
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        return self.page.locator(selector).get_attribute(attribute)
    
    def take_screenshot(self, path: str) -> None:
        self.page.screenshot(path=path)
    
    def get_current_url(self) -> str:
        return self.page.url
    
    def select_option(self, selector: str, value: str) -> None:
        self.page.select_option(selector, value)
    
    def get_all_text_contents(self, selector: str) -> list[str]:
        return self.page.locator(selector).all_text_contents()
