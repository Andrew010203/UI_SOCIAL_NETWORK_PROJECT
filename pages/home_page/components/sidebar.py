import allure
from base.base_page import BasePage
from config.links import Links


class SidebarComponent(BasePage):
    # Раздел Links
    _LINKS_POPUP_LOCATOR = ('xpath', '//li[contains(@class, "menu-section-links")]')
    # Содержимое раздела Links
    _NEWS_FEED_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-newsfeed"]')
    _FRIENDS_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-friends"]')
    _PHOTOS_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-photos"]')
    _NOTIFICATIONS_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-notifications"]')
    _MESSAGES_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-messages"]')
    _INVITE_FRIENDS_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-invite-friends"]')
    # Раздел Groups
    _GROUPS_POPUP_LOCATOR = ('xpath', '//li[contains(@class, "menu-section-groups")]')
    # Содержимое раздела Groups
    _ADD_GROUP_LOCATOR = ('xpath', '(//a[@id="ossn-group-add"])[1]')
    _MY_GROUPS_LOCATOR = ('xpath', '(//a[@id="ossn-group-add"])[2]')
    _GROUPS_LOCATOR = ('xpath', '//a[@class="menu-section-item-a-allgroups"]')
    # Раздел Site Members
    _SITE_MEMBERS_POPUP_LOCATOR = ('xpath', '//li[contains(@class, "menu-section-emembers")]')
    # Содержимое раздела Site Members
    _FEMALE_LOCATOR = ('xpath', '//li[@class="menu-section-item-emembers-female"]')
    _MALE_LOCATOR = ('xpath', '//li[@class="menu-section-item-emembers-male"]')
    # Раздел Videos
    _VIDEOS_POPUP_LOCATOR = ('xpath', '//li[contains(@class, "menu-section-videos")]')
    # Содержимое раздела Videos
    _ALL_SITE_VIDEOS_LOCATOR = ('xpath', '//li[@class="menu-section-item-videos-all"]')
    _MY_VIDEOS_LOCATOR = ('xpath', '//li[@class="menu-section-item-videos-my"]')
    _PENDING_LOCATOR = ('xpath', '//li[@class="menu-section-item-videos-pending"]')
    _ADD_VIDEO_LOCATOR = ('xpath', '//li[@class="menu-section-item-videos-add"]')

    @allure.step("Click on the link friends")
    def click_friends_link(self):
        self.ui_helper.click(self._FRIENDS_LOCATOR)

    @allure.step("Click menu item")
    def click_menu_item(self, menu_locator, submenu_locator):
        """
        Универсальный клик по подразделу с проверкой раскрытия родителя.
        """
        # 1. Пытаемся найти подраздел (ставим маленький таймаут, чтобы не ждать вечно)
        submenu = self.ui_helper.find(submenu_locator, timeout=2)
        # 2. Проверяем, можно ли с ним взаимодействовать
        if submenu and submenu.is_displayed():
            print("[DEBUG] Подраздел уже виден. Кликаю.")
            submenu.click()
        else:
            print("[DEBUG] Подраздел скрыт. Раскрываю родительское меню.")
            # Кликаем по родителю
            self.ui_helper.click(menu_locator)
            self.ui_helper.click(submenu_locator)

    @allure.step("Navigate to friends")
    def navigate_to_friends(self):
        # Метод сам знает свои локаторы, не надо их передавать из теста
        self.click_menu_item(self._LINKS_POPUP_LOCATOR, self._FRIENDS_LOCATOR)

    @allure.step("Click on the message icon")
    def click_message_icon(self):
        self.click_menu_item(self._LINKS_POPUP_LOCATOR, self._MESSAGES_LOCATOR)



