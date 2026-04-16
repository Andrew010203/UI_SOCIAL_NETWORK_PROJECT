import os
import random
import time
import pytest
import allure
from faker import Faker
from base.base_test import BaseTest

faker = Faker()


@allure.epic("Identity & Access")
@allure.feature("Successful registration with random data")
class TestRegistration(BaseTest):

    @pytest.mark.smoke
    @allure.story("New Account Creation")
    @allure.title("Registration")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration(self, driver):
        self.registration_page().open()
        self.registration_page().is_opened()
        unique_login = f"{faker.word()}+{random.randint(1000, 9999)}"
        unique_password = f"Qwe_{random.randint(1000, 9999)}_qwE"
        self.registration_page().registration_as_random_user(login=unique_login, password=unique_password)
        self.registration_page().ui_helper.screenshot("registration_success")


    # def test_registration_full_cycle(self, driver, email_helper):
    #     # 1. Подготовка данных
    #     inbox = email_helper.create_inbox()
    #     unique_login = f"user_{random.randint(1000, 9999)}"
    #     password = f"Pass_{random.randint(1000, 9999)}!QA"
    #
    #     # 2. Регистрация
    #     self.registration_page().open()
    #     self.registration_page().registration_as_random_user(
    #         login=unique_login,
    #         password=password,
    #         email=inbox["email"]  # Передаем почту из MailSlurp
    #     )
    #
    #     # 3. Ожидание письма и переход по ссылке
    #     email_data = email_helper.wait_for_email(inbox["id"])
    #     activation_link = email_helper.get_link(email_data["body"], keyword="verify")
    #
    #     assert activation_link, "Activation link not found in email body!"
    #
    #     driver.get(activation_link)
    #
    #     # 4. Финальный ассерт (зависит от сайта, обычно редирект на логин)
    #     # Пример: проверяем, что мы на странице логина и видим успех
    #     self.login_page().is_opened()
    #     # Тут можно добавить проверку сообщения "Account activated!"