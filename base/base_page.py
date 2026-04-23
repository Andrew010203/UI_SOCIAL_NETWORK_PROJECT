import allure
import json
from helpers.ui_helper import UIHelper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    _MESSAGE_NOTIFICATION = ("xpath", "//a[@class='ossn-notifications-messages']//span[@class='ossn-notification-container']")
    _SENDER_NAME = ("xpath", "//div[@class='ossn-notification-messages']//div[@class='name']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.ui_helper = UIHelper(self.driver)


    @allure.step("Open page")
    def open(self):
        self.driver.get(self._PAGE_URL)

    @allure.step("Check if page is opened")
    def is_opened(self, timeout=None):
        # self.wait.until(EC.url_to_be(self._PAGE_URL))
        self.wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout, poll_frequency=1)
        self.wait.until(EC.url_contains(self._PAGE_URL))

    def save_cookies(self, file_name="cookies.json"):
        # запись cookies
        with open(file_name, "w") as file:
            json.dump(self.driver.get_cookies(), file, indent=4)

    def load_cookies(self, file_name="cookies.json"):
        self.driver.delete_all_cookies()
        with open(file_name, "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry'])
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    @allure.step("Is new messages")
    def is_new_messages(self):
        notification = self.ui_helper.find(self._MESSAGE_NOTIFICATION, True)
        if int(notification.text) != 0:
            notification.click()

    @allure.step("Check message sender")
    def check_message_sender(self, expected_sender):
        sender = self.ui_helper.find(self._SENDER_NAME, wait=True)
        assert expected_sender in sender.text, f"Expected sender: {expected_sender}, but got {sender.text}"


    def click_menu_item(self, menu_item_locator, submenu_item_locator):
        # TODO: Доделать проверку на уже открытую страницу
        submenu_item = self.ui_helper.find(submenu_item_locator)
        if submenu_item.is_displayed():
            submenu_item.click()
        else:
            self.ui_helper.find(menu_item_locator).click()
            self.ui_helper.find(submenu_item_locator, wait=True).click()