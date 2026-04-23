import os
import time
import pytest
import allure
from faker import Faker
from base.base_test import BaseTest
from config.credentials import Credentials


faker = Faker()

@allure.epic("Identity & Access")
@allure.feature("Login")
class TestLogin(BaseTest):
    @pytest.mark.smoke
    @allure.story("Positive Login")
    @allure.title("Login as an existing user ('friend') via UI")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login(self, driver):
        self.login_page().open()
        self.login_page().is_opened(timeout=20)
        self.login_page().login_as("friend")
        self.login_page().save_cookies()
        self.home_page().is_opened()

    @pytest.mark.smoke
    @allure.story("Negaitive Login")
    @allure.title("Login with incorrect credentials (parametrized)")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("login, password, expected_error", [
        (Credentials.FRIEND_LOGIN, "wrong_psw" + faker.word(), "Invalid username or password"),  # Неверный пароль
        ("wrong_login" + faker.word(), Credentials.FRIEND_PASSWORD, "Invalid username or password"),  # Неверный логин

    ])
    def test_login_negative(self, driver, login, password, expected_error):
        self.login_page().open()
        self.login_page().is_opened()
        self.login_page().login_negative(login=login, password=password)
        # Проверка: текст ошибки должен содержать ожидаемую фразу
        actual_error = self.login_page().get_error_message()
        assert expected_error.lower() in actual_error.lower(), \
            f"Expected error '{expected_error}' not found in '{actual_error}'"



        #self.login_page().login_as("admin")
        # self.sidebar().business_page.create_new_business_page()
        # self.new_business_page().page_builder.set_page_name("QWE")
        # self.new_business_page().fill_required()
        # self.new_business_page().is_page_created()



