import pytest
import allure
from faker import Faker
from base.base_test import BaseTest
from pages.home_page.page import HomePage
from pages.messages_page.page import MessagesPage

faker = Faker()


@allure.epic("Social Engine")
@allure.feature("Messages")
class TestMessage(BaseTest):
    @pytest.mark.smoke
    @allure.story("Send message")
    @allure.title("Send a message from Admin and verify receipt by Friend")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_send_message(self, admin_browser, friend_browser):
        # Инициализируем страницы для каждого браузера отдельно
        admin_home = HomePage(admin_browser)
        admin_messages = MessagesPage(admin_browser)

        friend_home = HomePage(friend_browser)
        friend_messages = MessagesPage(friend_browser)

        # 1. ДЕЙСТВИЕ В ОКНЕ АДМИНА
        admin_home.open()  # Открываем главную (он уже залогинен по кукам!)
        admin_home.choice_companion("Bob Black")
        admin_messages.click_message_button()
        message_text = faker.text()
        admin_messages.write_message(message_text)

        # 2. ПРОВЕРКА В ОКНЕ ДРУГА (Оно открыто параллельно!)
        friend_home.open()  # Открываем главную у друга
        friend_home.sidebar.click_menu_item(
            friend_home.sidebar._LINKS_POPUP_LOCATOR,
            friend_home.sidebar._MESSAGES_LOCATOR
        )
        friend_messages.is_opened()

        # Проверка последнего сообщения в окне друга
        actual_text = friend_messages.get_last_received_message_text()
        assert message_text.strip() in actual_text.strip(), \
            f"Ожидали сообщение '{message_text}', но последнее в чате: '{actual_text}'"



