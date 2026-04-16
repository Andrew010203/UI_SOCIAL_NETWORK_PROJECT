import os
import time
import pytest
import allure
from faker import Faker
from base.base_test import BaseTest


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
        self.login_page().is_opened()
        self.login_page().login_as("friend")
        self.login_page().save_cookies()
        #self.home_page().is_opened()  # проверка что открылась homepage позже допилится когда

        #self.login_page().login_as("admin")
        # self.sidebar().business_page.create_new_business_page()
        # self.new_business_page().page_builder.set_page_name("QWE")
        # self.new_business_page().fill_required()
        # self.new_business_page().is_page_created()



