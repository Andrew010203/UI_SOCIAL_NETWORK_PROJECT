import pytest
import allure
from faker import Faker
from base.base_test import BaseTest

faker = Faker()


@allure.epic("Social Engine")
@allure.feature("Wall Posts")
class TestWall(BaseTest):
    @pytest.mark.smoke
    @allure.story("Creating Posts")
    @allure.title("Create a new text post in News Feed")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_post(self, driver):
        # 1. UI-авторизация
        self.login_page().open()
        self.login_page().is_opened()
        self.login_page().login_as("friend")
        # 2. Проверяем, что нас пустило на Home Page
        self.home_page().is_opened()
        # 3. Подготовка текста поста
        post_text = faker.sentence()
        # 4. Публикация поста
        self.home_page().publish_post(post_text)
        # 5. Проверка публикации написанного поста
        actual_post = self.home_page().get_latest_post_text()
        assert post_text in actual_post, f"Ожидали текст '{post_text}', но увидели '{actual_post}'"
        # 6. Удаление опубликованного поста
        self.home_page().delete_post()
        # 7. Проверка удаления поста
        is_deleted = self.home_page().wait_post_disappear(actual_post)
        assert is_deleted, "Пост не исчез после удаления!"



