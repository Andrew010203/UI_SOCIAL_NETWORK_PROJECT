from pages.login_page.page import LoginPage
from selenium.webdriver.remote.webdriver import WebDriver
from pages.registration_page.page import RegistrationPage


# from pages.news_feed_page.page import NewsFeedPage
# from base_components.sidebar.sidebar import Sidebar
# from pages.new_business_page.page import CreateNewBusinessPage
# from pages.messages_page.page import MessagesPage

class BaseTest:
    driver: WebDriver

    def setup_method(self):
        # Pages
        self.login_page = lambda driver=self.driver: LoginPage(driver)
        self.registration_page = lambda driver=self.driver: RegistrationPage(driver)
        # self.news_feed_page = lambda driver=self.driver: NewsFeedPage(driver)
        # self.new_business_page = lambda driver=self.driver: CreateNewBusinessPage(driver)
        # self.messages_page = lambda driver=self.driver: MessagesPage(driver)
        #
        # # Components
        # self.sidebar = lambda driver=self.driver: Sidebar(driver)