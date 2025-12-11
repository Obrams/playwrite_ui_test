import pytest
import allure
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from utils.test_data import PRODUCTS, SORT_OPTIONS


@allure.epic("E-commerce")
@allure.feature("Каталог товаров")
@pytest.mark.inventory
class TestInventory:
    
    @allure.story("Отображение товаров")
    @allure.title("Проверка отображения всех товаров в каталоге")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_products_displayed(self, authenticated_user: InventoryPage):
        with allure.step("Проверяем количество отображаемых товаров"):
            products_count = authenticated_user.get_products_count()
            allure.attach(str(products_count), "Количество товаров", allure.attachment_type.TEXT)
            assert products_count == 6
    
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, authenticated_user: InventoryPage):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        
        assert authenticated_user.is_cart_badge_visible()
        cart_count = authenticated_user.get_cart_badge_count()
        assert cart_count == "1"
    
    @pytest.mark.regression
    def test_add_multiple_products(self, authenticated_user: InventoryPage):
        products_to_add = [
            PRODUCTS["backpack"],
            PRODUCTS["bike_light"],
            PRODUCTS["bolt_tshirt"]
        ]
        
        for product in products_to_add:
            authenticated_user.add_product_to_cart(product)
        
        cart_count = authenticated_user.get_cart_badge_count()
        assert cart_count == "3"
    
    @pytest.mark.regression
    def test_remove_product_from_inventory(self, authenticated_user: InventoryPage):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        assert authenticated_user.is_cart_badge_visible()
        
        authenticated_user.remove_product_from_cart(PRODUCTS["backpack"])
        assert not authenticated_user.is_cart_badge_visible()
    
    @pytest.mark.smoke
    def test_sort_by_name_a_to_z(self, authenticated_user: InventoryPage):
        authenticated_user.sort_products(SORT_OPTIONS["name_asc"])
        product_names = authenticated_user.get_product_names()
        
        sorted_names = sorted(product_names)
        assert product_names == sorted_names
    
    @pytest.mark.regression
    def test_sort_by_name_z_to_a(self, authenticated_user: InventoryPage):
        authenticated_user.sort_products(SORT_OPTIONS["name_desc"])
        product_names = authenticated_user.get_product_names()
        
        sorted_names = sorted(product_names, reverse=True)
        assert product_names == sorted_names
    
    @pytest.mark.smoke
    def test_sort_by_price_low_to_high(self, authenticated_user: InventoryPage):
        authenticated_user.sort_products(SORT_OPTIONS["price_asc"])
        product_prices = authenticated_user.get_product_prices()
        
        sorted_prices = sorted(product_prices)
        assert product_prices == sorted_prices
    
    @pytest.mark.regression
    def test_sort_by_price_high_to_low(self, authenticated_user: InventoryPage):
        authenticated_user.sort_products(SORT_OPTIONS["price_desc"])
        product_prices = authenticated_user.get_product_prices()
        
        sorted_prices = sorted(product_prices, reverse=True)
        assert product_prices == sorted_prices
    
    @pytest.mark.smoke
    def test_cart_badge_updates(self, authenticated_user: InventoryPage):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        assert authenticated_user.get_cart_badge_count() == "1"
        
        authenticated_user.add_product_to_cart(PRODUCTS["bike_light"])
        assert authenticated_user.get_cart_badge_count() == "2"
        
        authenticated_user.remove_product_from_cart(PRODUCTS["backpack"])
        assert authenticated_user.get_cart_badge_count() == "1"
    
    @pytest.mark.regression
    def test_navigation_to_cart(self, authenticated_user: InventoryPage, page: Page):
        authenticated_user.add_product_to_cart(PRODUCTS["backpack"])
        authenticated_user.go_to_cart()
        
        page.wait_for_url("**/cart.html")
