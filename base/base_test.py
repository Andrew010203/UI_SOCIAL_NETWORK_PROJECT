from pages.friends_page.page import FriendsPage
from pages.login_page.page import LoginPage
from selenium.webdriver.remote.webdriver import WebDriver
from pages.messages_page.page import MessagesPage
from pages.registration_page.page import RegistrationPage
from pages.home_page.page import HomePage


class BaseTest:
    driver: WebDriver

    def setup_method(self):
        # Pages
        self.login_page = lambda driver=self.driver: LoginPage(driver)
        self.registration_page = lambda driver=self.driver: RegistrationPage(driver)
        self.home_page = lambda driver=self.driver: HomePage(driver)
        self.friends_page = lambda driver=self.driver: FriendsPage(driver)
        self.messages_page = lambda driver=self.driver: MessagesPage(driver)

