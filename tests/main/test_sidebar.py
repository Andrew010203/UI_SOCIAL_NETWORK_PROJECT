import pytest
import allure
from faker import Faker
from base.base_test import BaseTest

faker = Faker()


@allure.epic("Social Engine")
@allure.feature("Navigation")
class TestSidebar(BaseTest):
    @pytest.mark.smoke
    @allure.story("Sidebar Links")
    @allure.title("Navigate to Friends page via Sidebar")
    @allure.severity(allure.severity_level.NORMAL)
    def test_go_to_the_friends_page(self, driver):
        # 1. Авторизация (используем уже созданного юзера)
        self.login_page().open()
        self.login_page().is_opened()
        self.login_page().login_as("friend")
        # 2. Переход на страницу home
        self.home_page().open()
        self.home_page().is_opened()
        # 3. Навигация по sidebar
        self.home_page().sidebar.navigate_to_friends()
        # 4. Проверка открытия friends_page
        self.friends_page().is_opened()
        # 5. Проверка заголовок Friends присутствует
        self.friends_page().title_is_visible()
