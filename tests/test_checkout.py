import pytest
import allure
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_complete_page import CheckoutCompletePage
from utils.test_data import PRODUCTS, TEST_CHECKOUT_DATA, SUCCESS_MESSAGES


@allure.epic("E-commerce")
@allure.feature("Оформление заказа")
@pytest.mark.checkout
class TestCheckout:
    
    @allure.story("E2E покупка товара")
    @allure.title("Полный цикл покупки товара от каталога до завершения заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_complete_purchase_flow(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        checkout_complete_page: CheckoutCompletePage,
        page: Page
    ):
        with allure.step("Добавляем товар в корзину"):
            authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        
        with allure.step("Переходим в корзину"):
            authenticated_user.go_to_cart()
        
        with allure.step("Переходим к оформлению заказа"):
            cart_page.proceed_to_checkout()
        
        with allure.step("Заполняем данные для доставки"):
            checkout_data = TEST_CHECKOUT_DATA["valid"]
            checkout_page.fill_checkout_info(
                checkout_data["first_name"],
                checkout_data["last_name"],
                checkout_data["postal_code"]
            )
            checkout_page.click_continue()
            page.wait_for_url("**/checkout-step-two.html")
        
        with allure.step("Завершаем оформление заказа"):
            checkout_page.finish_checkout()
            page.wait_for_url("**/checkout-complete.html")
        
        with allure.step("Проверяем успешное завершение заказа"):
            assert checkout_complete_page.is_order_complete()
            success_header = checkout_complete_page.get_success_header()
            allure.attach(success_header, "Заголовок успеха", allure.attachment_type.TEXT)
            assert SUCCESS_MESSAGES["header"] in success_header
    
    @pytest.mark.regression
    def test_checkout_with_empty_first_name(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["invalid_first_name"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed()
        error_message = checkout_page.get_error_message()
        assert checkout_data["expected_error"] in error_message
    
    @pytest.mark.regression
    def test_checkout_with_empty_last_name(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["invalid_last_name"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed()
        error_message = checkout_page.get_error_message()
        assert checkout_data["expected_error"] in error_message
    
    @pytest.mark.regression
    def test_checkout_with_empty_postal_code(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["invalid_postal_code"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed()
        error_message = checkout_page.get_error_message()
        assert checkout_data["expected_error"] in error_message
    
    @pytest.mark.regression
    def test_cancel_checkout_step_one(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        page: Page
    ):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_page.click_cancel()
        
        page.wait_for_url("**/cart.html")
    
    @pytest.mark.smoke
    def test_price_calculation(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        products = [PRODUCTS["backpack"], PRODUCTS["bike_light"]]
        for product in products:
            authenticated_user.add_product_to_cart(product)
        
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["valid"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        order_summary = checkout_page.get_order_summary()
        assert order_summary["subtotal"] > 0
        assert order_summary["tax"] > 0
        assert order_summary["total"] > 0
        
        expected_total = round(order_summary["subtotal"] + order_summary["tax"], 2)
        actual_total = round(order_summary["total"], 2)
        assert expected_total == actual_total
    
    @pytest.mark.regression
    def test_checkout_items_count(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage
    ):
        products = [
            PRODUCTS["backpack"],
            PRODUCTS["bike_light"],
            PRODUCTS["bolt_tshirt"]
        ]
        for product in products:
            authenticated_user.add_product_to_cart(product)
        
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["valid"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        items_count = checkout_page.get_items_count()
        assert items_count == 3
    
    @pytest.mark.regression
    def test_back_to_products_after_complete(
        self, 
        authenticated_user: InventoryPage, 
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        checkout_complete_page: CheckoutCompletePage,
        page: Page
    ):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_data = TEST_CHECKOUT_DATA["valid"]
        checkout_page.fill_checkout_info(
            checkout_data["first_name"],
            checkout_data["last_name"],
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        checkout_page.finish_checkout()
        checkout_complete_page.back_to_products()
        
        page.wait_for_url("**/inventory.html")
