import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver import Keys


class MessagesPage(BasePage):

    _PAGE_URL = Links.MESSAGE_PAGE
    _SEARCH_FIELD = ("xpath", '(//input[@type="text"])[2]')
    _ADD_FRIEND_BUTTON = ("xpath", '//div/a[text()="Add Friend"]')
    _MESSAGE_BUTTON_LOCATOR = ("xpath", '//div/a[@id="profile-message"]')
    _MESSAGE_FIELD_LOCATOR = ("xpath", '//textarea[@name="message"]')
    _SEND_BUTTON_LOCATOR = ("xpath", '//div/input[@type="submit"]')
    _LAST_MESSAGE_LOCATOR = ("xpath", '(//div[starts-with(@id, "message-item-")])[last()]')

    @allure.step("Search companion: {text}")
    def search_companion(self, text):
        search_field = self.ui_helper.find(self._SEARCH_FIELD)
        self.ui_helper.fill(self._SEARCH_FIELD, text=text)
        search_field.send_keys(Keys.ENTER)

    @allure.step("Click add friend button")
    def add_friend(self):
        self.ui_helper.find(self._ADD_FRIEND_BUTTON).click()

    @allure.step("Click message button to open chat")
    def click_message_button(self):
        self.ui_helper.click(self._MESSAGE_BUTTON_LOCATOR)

    @allure.step("Write and send message: {message}")
    def write_message(self, message: str):
        self.ui_helper.fill(self._MESSAGE_FIELD_LOCATOR, message)
        self.ui_helper.click(self._SEND_BUTTON_LOCATOR)

    @allure.step("Get text of the last received message")
    def get_last_received_message_text(self):
        """Ожидаем сообщение"""
        post_text = self.ui_helper.find(self._LAST_MESSAGE_LOCATOR, wait=True).text
        return post_text
