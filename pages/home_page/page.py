import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials
from pages.home_page.components.sidebar import SidebarComponent


class HomePage(BasePage):

    _PAGE_URL = Links.HOME_PAGE

    _POST_FIELD_LOCATOR = ('xpath', '//textarea[@placeholder="What\'s on your mind?"]')
    _POST_BUTTON_LOCATOR = ('xpath', '//input[@value="Post"]')
    _NEW_POST_TEXT = ('xpath', '//div[@post="new"]//p')
    _EDIT_NEW_POST_BUTTON_LOCATOR = ('xpath', '(//div[@class="post-menu"])[1]')
    _DELETE_LOCATOR = ('xpath', '//a[text()="Delete"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)

    @allure.step("Waiting for the post to disappear")
    def wait_post_disappear(self, text):
        # Динамический локатор для конкретного текста
        locator = ("xpath", f"//p[contains(text(), '{text}')]")
        return self.ui_helper.wait_for_invisibility(locator)

    @allure.step("Publishing a post")
    def publish_post(self, text):
        self.ui_helper.fill(locator=self._POST_FIELD_LOCATOR, text=text)
        self.ui_helper.click(locator=self._POST_BUTTON_LOCATOR)

    @allure.step("Getting the text of the latest publication")
    def get_latest_post_text(self):
        post_text = self.ui_helper.find(self._NEW_POST_TEXT, wait=True).text
        return post_text

    @allure.step("Deleting publication")
    def delete_post(self):
        self.ui_helper.click(self._EDIT_NEW_POST_BUTTON_LOCATOR)
        self.ui_helper.click(self._DELETE_LOCATOR)

    @allure.step("Choice of companion")
    def choice_companion(self, name: str):
        locator = ('xpath', f'//div[@class="widget-contents"]/a[@title="{name}"]')
        self.ui_helper.click(locator)






