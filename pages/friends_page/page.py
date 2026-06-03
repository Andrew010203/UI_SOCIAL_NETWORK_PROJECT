import allure
from base.base_page import BasePage
from config.links import Links


class FriendsPage(BasePage):

    #_PAGE_URL = Links.FRIENDS_PAGE
    _PAGE_URL = "/friends"
    _TITLE_FRIENDS_LOCATOR = ('xpath', '//div[text()="Friends"]')

    @allure.step("Title is visible")
    def title_is_visible(self):
        self.ui_helper.wait_for_visibility(self._TITLE_FRIENDS_LOCATOR)
