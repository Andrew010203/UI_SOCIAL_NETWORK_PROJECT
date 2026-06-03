import time
import allure
from faker import Faker
import platform
import datetime

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

faker = Faker()


class UIHelper:

    # os_name = platform.system()
    # CMD_CTRL = Keys.COMMAND if os_name == "darwin" else Keys.CONTROL

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.actions = ActionChains(self.driver)

    def find(self, locator: tuple, message: str = "", wait: bool = False, timeout: int = None) -> WebElement:
        """Поиск одного элемента с динамическими ожиданиями"""
        if timeout:
            # Если передан таймаут, создаем временное ожидание
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator), message=message)
        if wait:
            element = self.wait.until(EC.visibility_of_element_located(locator), message=message)
        else:
            element = self.driver.find_element(*locator)
        return element

    def find_all(self, locator: tuple, message: str = "", wait: bool = True) -> list[WebElement]:
        """Поиск коллекции элементов"""
        if wait:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator), message=message)
        else:
            elements = self.driver.find_elements(*locator)
        return elements

    def fill(self, locator: tuple, text: str):
        """Безопасное заполнение поля ввода с предварительной очисткой"""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator: tuple, message: str = ""):
        """Клик по элементу, когда он гарантированно кликабелен"""
        self.wait.until(EC.element_to_be_clickable(locator), message=message).click()

    def screenshot(self, name: str = "screenshot"):
        """Снятие скриншота и прикрепление его к отчету Allure"""
        # Создаём имя: название_теста_2023-10-27_15-30-05
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = f"{name}_{timestamp}"
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

    def wait_for_invisibility(self, locator: tuple, message: str = "") -> WebElement:
        """Ожидание исчезновения элемента с экрана"""
        element = self.wait.until(EC.invisibility_of_element_located(locator), message=message)
        return element

    def wait_for_visibility(self, locator: tuple, message: str = "") -> WebElement:
        """Ожидание появления элемента на экране"""
        element = self.wait.until(EC.visibility_of_element_located(locator), message=message)
        return element

    def wait_for_text_in_web_element(self, element, text: str, message: str = None):
        """
        Ожидает появления текста в веб-элементе.

        :param element: Веб-элемент, в котором будем искать текст.
        :param text: Текст, который мы ожидаем найти в элементе.
        :param message: Сообщение об ошибке, если текст не найден.
        :return: Возвращает элемент, если текст найден.
        """
        try:
            # Ожидаем появления текста в элементе
            self.wait.until(lambda driver: text in element.text)
            return element
        except Exception as e:
            if message:
                raise TimeoutException(message)
            raise e

    def scroll_by(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y})")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_element(self, locator):
        self.actions.scroll_to_element(self.find(locator))
        self.driver.execute_script("""
        window.scrollTo({
            top: window.scrollY + 500,
        });
        """)

    def click_via_js(self, locator: tuple):
        """Клик силами JavaScript в обход перекрывающих элементов DOM"""
        element = self.find(locator, wait=True)
        self.driver.execute_script("arguments[0].click();", element)


