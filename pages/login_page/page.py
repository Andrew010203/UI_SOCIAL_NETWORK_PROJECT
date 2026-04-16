import time

import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials


class LoginPage(BasePage):

    _PAGE_URL = Links.LOGIN_PAGE

    _LOGIN_BUTTON = ("xpath", "//input[@type='submit']")
    _LOGIN_FIELD = ("xpath", "//input[@name='username']")
    _PASSWORD_FIELD = ("xpath", "//input[@name='password']")

    @allure.step("Click login button")
    def login_as(self, user_type):
        if user_type == "admin":
            self.ui_helper.fill(locator=self._LOGIN_FIELD, text=Credentials.ADMIN_LOGIN)
            self.ui_helper.fill(locator=self._PASSWORD_FIELD, text=Credentials.ADMIN_PASSWORD)
            self.ui_helper.click(self._LOGIN_BUTTON, "Login button")
        elif user_type == "friend":
            self.ui_helper.fill(locator=self._LOGIN_FIELD, text=Credentials.FRIEND_LOGIN)
            self.ui_helper.fill(locator=self._PASSWORD_FIELD, text=Credentials.FRIEND_PASSWORD)
            self.ui_helper.click(self._LOGIN_BUTTON, "Login button")