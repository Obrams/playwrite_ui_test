import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_complete_page import CheckoutCompletePage
from utils.test_data import BASE_URL, VALID_USERS
from pathlib import Path
from datetime import datetime


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,
        "locale": "ru-RU",
    }


@pytest.fixture(scope="session", autouse=True)
def create_screenshots_dir():
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    allure_results_dir = Path("allure-results")
    allure_results_dir.mkdir(exist_ok=True)
    
    return screenshots_dir


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.navigate_to(BASE_URL)
    return login_page


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def authenticated_user(page: Page, login_page: LoginPage, inventory_page: InventoryPage):
    user = VALID_USERS["standard_user"]
    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/inventory.html")
    return inventory_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def handle_test_failure(request, page: Page, create_screenshots_dir):
    yield
    
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = create_screenshots_dir / f"{test_name}_{timestamp}.png"
        
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            
            with open(screenshot_path, 'rb') as screenshot_file:
                allure.attach(
                    screenshot_file.read(),
                    name=f"Screenshot_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception:
            pass


@pytest.fixture
def clean_cart(authenticated_user, cart_page: CartPage):
    yield authenticated_user
    
    try:
        authenticated_user.go_to_cart()
        if cart_page.get_cart_items_count() > 0:
            for item_name in cart_page.get_cart_item_names():
                cart_page.remove_item(item_name)
    except Exception:
        pass


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Smoke тесты")
    config.addinivalue_line("markers", "regression: Regression тесты")
    config.addinivalue_line("markers", "login: Тесты авторизации")
    config.addinivalue_line("markers", "cart: Тесты корзины")
    config.addinivalue_line("markers", "checkout: Тесты оформления")
    config.addinivalue_line("markers", "inventory: Тесты каталога")
