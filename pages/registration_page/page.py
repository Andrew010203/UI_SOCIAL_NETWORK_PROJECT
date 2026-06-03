import allure
import random
import pytest
from faker import Faker
from base.base_page import BasePage
from config.links import Links

faker = Faker()


class RegistrationPage(BasePage):
    _PAGE_URL = Links.HOST

    _FIRST_NAME_FIELD = ('xpath', '//input[@name="firstname"]')
    _LAST_NAME_FIELD = ('xpath', '//input[@name="lastname"]')
    _EMAIL_FIELD = ('xpath', '//input[@name="email"]')
    _RE_ENTER_EMAIL_FIELD = ('xpath', '//input[@name="email_re"]')
    _USERNAME_FIELD = ('xpath', '(//input[@name="username"])[2]')
    _PASSWORD_FIELD = ('xpath', '(//input[@name="password"])[2]')
    _BIRTHDATE_FIELD = ('xpath', '//input[@name="birthdate"]')
    _MALE_RADIO_BUTTON = ('xpath', '//input[@value="male"]')
    _FEMALE_RADIO_BUTTON = ('xpath', '//span[text()="Female"]')
    _CONFIRM_CHECK_BOX = ('xpath', '//input[@name="gdpr_agree"]')
    _CREATE_AN_ACCOUNT_BUTTON = ('xpath', '//input[@value="Create an account"]')
    _LOGIN_BUTTON = ('xpath', '(//a[text()="Login"])[1]')
    _RESET_PASSWORD_BUTTON = ('xpath', '//input[@value="Login"]')
    _MONTH_set = ('xpath', '//select[@class="ui-datepicker-month"]/option[normalize-space(text())="May"]')
    _SET_YEAR = ('xpath', '(//td[@data-year="2025"])[9]')
    _YEAR_FIELD = ('xpath', '//select[@class="ui-datepicker-year"]')
    _YEAR_BUTTON = ('xpath', f'//option[normalize-space(text())="{None}"]')
    _MONTH_FIELD = ('xpath', '//select[@class="ui-datepicker-month"]')
    _MONTH_BUTTON = ('xpath', f'//option[@value="{None}"]')
    _DAY_LOCATOR = ('xpath', f'//a[normalize-space(text())="{None}"]')
    _SET_DAY = ('xpath', '//a[@data-date="9"]')
    _LOGIN_BUTTON_ADMIN = ('xpath', '//input[@value="Login"]')
    _MESSAGE_REG_NOTIFICATION = ('xpath', '//div[@class="ossn-message-done"]')
    _ERROR_MESSAGE = ("xpath", '//div[@id="ossn-signup-errors"]')

    _MONTH_POPUP = ('xpath', '//select[@class="ui-datepicker-month"]')

    # def __init__(self, driver):
    #     super().__init__(driver)
    # self.login_page = LoginPage(driver)
    # self.date_picker_helper = DatePickerHelper(driver)

    def open_date_picker(self):
        """Метод открытия date picker"""
        self.ui_helper.click(self._BIRTHDATE_FIELD)

    def set_year(self, year: int):
        """Метод ввода года"""
        self.ui_helper.click(self._YEAR_FIELD)
        year_option = ('xpath', f'//option[normalize-space(text())="{year}"]')
        self.ui_helper.click(year_option)

    def set_month(self, month_number: int):
        """Метод ввода месяца"""
        self.ui_helper.click(self._MONTH_FIELD)
        month_option = ('xpath', f'//option[@value="{month_number - 1}"]')
        self.ui_helper.click(month_option)

    def set_day(self, day_number: int):
        """Метод ввода дня"""
        day_locator = ('xpath', f'//a[normalize-space(text())="{day_number}"]')
        self.ui_helper.click(day_locator)

    @allure.step("Get error message text")
    def get_error_message(self):
        # Ждём появления и возвращаем текст
        return self.ui_helper.wait_for_visibility(self._ERROR_MESSAGE).text

    @allure.step("Get successful registration message text")
    def get_success_message(self):
        """Возвращаем текст сообщения для проверки в тесте"""
        return self.ui_helper.wait_for_visibility(
            self._MESSAGE_REG_NOTIFICATION,
            message="Your account has been registered!"
        ).text

    def _fill_registration_form(self, login: str, password: str, email: str):
        """Вспомогательный скрытый метод заполнения всей анкеты"""
        # Заполнение полей
        self.ui_helper.fill(self._FIRST_NAME_FIELD, faker.first_name())
        self.ui_helper.fill(self._LAST_NAME_FIELD, faker.last_name())
        self.ui_helper.fill(self._EMAIL_FIELD, email)
        self.ui_helper.fill(self._RE_ENTER_EMAIL_FIELD, email)
        self.ui_helper.fill(self._USERNAME_FIELD, login)
        self.ui_helper.fill(self._PASSWORD_FIELD, password)
        # Работа с date_picker
        self.open_date_picker()
        self.set_year(random.randint(1900, 2007))
        self.set_month(random.randint(1, 12))
        self.set_day(random.randint(1, 28))
        # Выбор пола и согласие
        self.ui_helper.click(self._MALE_RADIO_BUTTON)
        self.ui_helper.click(self._CONFIRM_CHECK_BOX)

    @allure.step("Registration as random user with email: {email}")
    def registration_as_random_user(self, login: str, password: str, email: str):
        self._fill_registration_form(login, password, email)
        self.ui_helper.click(self._CREATE_AN_ACCOUNT_BUTTON)

    @allure.step("Registration with invalid data")
    def registration_negative(self, login: str, password: str, email: str):
        self._fill_registration_form(login, password, email)
        self.ui_helper.click(self._CREATE_AN_ACCOUNT_BUTTON)

