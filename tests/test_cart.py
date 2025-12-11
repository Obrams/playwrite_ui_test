import pytest
import allure
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.test_data import PRODUCTS, INVENTORY_URL


@allure.epic("E-commerce")
@allure.feature("Корзина")
@pytest.mark.cart
class TestCart:
    
    @allure.story("Просмотр товаров в корзине")
    @allure.title("Просмотр одного товара в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_view_cart_items(self, authenticated_user: InventoryPage, cart_page: CartPage):
        product_name = PRODUCTS["backpack"]
        
        with allure.step(f"Добавляем товар '{product_name}' в корзину"):
            authenticated_user.add_product_to_cart(product_name)
        
        with allure.step("Переходим в корзину"):
            authenticated_user.go_to_cart()
        
        with allure.step("Проверяем количество товаров в корзине"):
            items_count = cart_page.get_cart_items_count()
            assert items_count == 1, f"Ожидался 1 товар в корзине, найдено: {items_count}"
        
        with allure.step("Проверяем наличие товара в корзине"):
            cart_items = cart_page.get_cart_item_names()
            assert product_name in cart_items, \
                f"Товар {product_name} не найден в корзине. Товары в корзине: {cart_items}"
    
    @pytest.mark.regression
    def test_view_multiple_cart_items(self, authenticated_user: InventoryPage, cart_page: CartPage):
        products_to_add = [
            PRODUCTS["backpack"],
            PRODUCTS["bike_light"],
            PRODUCTS["bolt_tshirt"]
        ]
        
        for product in products_to_add:
            authenticated_user.add_product_to_cart(product)
        
        authenticated_user.go_to_cart()
        
        items_count = cart_page.get_cart_items_count()
        assert items_count == 3, f"Ожидалось 3 товара в корзине, найдено: {items_count}"
        
        cart_items = cart_page.get_cart_item_names()
        for product in products_to_add:
            assert product in cart_items, f"Товар {product} не найден в корзине"
    
    @allure.story("Удаление товаров из корзины")
    @allure.title("Удаление товара из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_remove_item_from_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        product_name = PRODUCTS["backpack"]
        
        with allure.step(f"Добавляем товар '{product_name}' в корзину"):
            authenticated_user.add_product_to_cart(product_name)
            authenticated_user.go_to_cart()
        
        with allure.step("Проверяем что товар добавлен"):
            assert cart_page.get_cart_items_count() == 1
        
        with allure.step("Удаляем товар из корзины"):
            cart_page.remove_item(product_name)
        
        with allure.step("Проверяем что корзина пуста"):
            assert cart_page.is_cart_empty()
    
    @pytest.mark.regression
    def test_remove_one_of_multiple_items(self, authenticated_user: InventoryPage, cart_page: CartPage):
        products = [PRODUCTS["backpack"], PRODUCTS["bike_light"]]
        for product in products:
            authenticated_user.add_product_to_cart(product)
        
        authenticated_user.go_to_cart()
        cart_page.remove_item(PRODUCTS["backpack"])
        
        assert cart_page.get_cart_items_count() == 1
        cart_items = cart_page.get_cart_item_names()
        assert PRODUCTS["bike_light"] in cart_items
        assert PRODUCTS["backpack"] not in cart_items
    
    @pytest.mark.smoke
    def test_continue_shopping(self, authenticated_user: InventoryPage, cart_page: CartPage, page: Page):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.continue_shopping()
        
        expect(page).to_have_url(INVENTORY_URL)
    
    @pytest.mark.smoke
    def test_empty_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        authenticated_user.go_to_cart()
        assert cart_page.is_cart_empty()
    
    @pytest.mark.regression
    def test_cart_item_prices(self, authenticated_user: InventoryPage, cart_page: CartPage):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        
        prices = cart_page.get_cart_item_prices()
        assert len(prices) > 0
        for price in prices:
            assert price > 0
    
    @pytest.mark.regression
    def test_proceed_to_checkout(self, authenticated_user: InventoryPage, cart_page: CartPage, page: Page):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        page.wait_for_url("**/checkout-step-one.html")
