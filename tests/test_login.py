import pytest
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.test_data import VALID_USERS, INVALID_CREDENTIALS, INVENTORY_URL


@allure.epic("E-commerce")
@allure.feature("Авторизация")
@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    
    @allure.story("Успешная авторизация")
    @allure.title("Успешная авторизация стандартного пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, page: Page, login_page: LoginPage):
        user = VALID_USERS["standard_user"]
        
        with allure.step(f"Выполняем вход с логином: {user['username']}"):
            login_page.login(user["username"], user["password"])
        
        with allure.step("Проверяем редирект на страницу каталога"):
            expect(page).to_have_url(INVENTORY_URL)
    
    @allure.story("Негативные сценарии")
    @allure.title("Попытка входа заблокированным пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_locked_out_user(self, page: Page, login_page: LoginPage):
        user = VALID_USERS["locked_out_user"]
        
        with allure.step(f"Выполняем вход с заблокированным пользователем: {user['username']}"):
            login_page.login(user["username"], user["password"])
        
        with allure.step("Проверяем отображение ошибки"):
            assert login_page.is_error_displayed()
        
        with allure.step("Проверяем текст ошибки о блокировке"):
            error_message = login_page.get_error_message()
            allure.attach(error_message, "Сообщение об ошибке", allure.attachment_type.TEXT)
            assert "locked out" in error_message.lower()
    
    @pytest.mark.regression
    @pytest.mark.parametrize("credentials", INVALID_CREDENTIALS)
    def test_invalid_credentials(self, page: Page, login_page: LoginPage, credentials: dict):
        login_page.login(credentials["username"], credentials["password"])
        assert login_page.is_error_displayed()
        
        error_message = login_page.get_error_message()
        assert credentials["expected_error"] in error_message
    
    @pytest.mark.regression
    def test_empty_username(self, page: Page, login_page: LoginPage):
        login_page.login("", "secret_sauce")
        assert login_page.is_error_displayed()
        
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message
    
    @pytest.mark.regression
    def test_empty_password(self, page: Page, login_page: LoginPage):
        login_page.login("standard_user", "")
        assert login_page.is_error_displayed()
        
        error_message = login_page.get_error_message()
        assert "Password is required" in error_message
    
    @pytest.mark.smoke
    def test_login_page_elements(self, login_page: LoginPage):
        assert login_page.is_visible(login_page.USERNAME_INPUT)
        assert login_page.is_visible(login_page.PASSWORD_INPUT)
        assert login_page.is_visible(login_page.LOGIN_BUTTON)
