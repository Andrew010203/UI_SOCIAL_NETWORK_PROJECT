import os
import random
import time
import pytest
import allure
from faker import Faker
from base.base_test import BaseTest
from config.credentials import Credentials

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

    @pytest.mark.smoke
    @allure.story("New Account Creation")
    @allure.title("Registration (negative)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("email, login, password, expected_error", [
        (Credentials.FRIEND_EMAIL, "unique_user_" + faker.word(),
         Credentials.FRIEND_PASSWORD, "already exists in our database"),  # Существующий Email в базе
        (faker.email(), Credentials.FRIEND_LOGIN,
         Credentials.FRIEND_PASSWORD, "username is taken"),  # Существующий login в базе
        ("invalid-email.com", "random_user",
         Credentials.FRIEND_PASSWORD, "Email address is invalid"),  # Невалидный формат Email в базе
        (faker.email(), "short_pass_user", "123", "password does not meet the requirements")  # Короткий пароль
    ])
    def test_registration_negative(self, driver, email, login, password, expected_error):
        self.registration_page().open()
        self.registration_page().is_opened()
        self.registration_page().registration_negative(login=login, password=password, email=email)
        # Проверка: текст ошибки должен содержать ожидаемую фразу
        actual_error = self.registration_page().get_error_message()
        assert expected_error.lower() in actual_error.lower(), \
            f"Expected error '{expected_error}' not found in '{actual_error}'"

        #self.registration_page().ui_helper.screenshot("registration_success") # этот шаг не нужен(есть хук)


  # // div[contains(@class, 'ossn-message-error')]
#
#
#     Текст ошибки: 'Invalid username or password!
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