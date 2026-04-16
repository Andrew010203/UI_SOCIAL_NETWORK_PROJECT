import time
import allure
from faker import Faker
import platform
import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver import Keys

faker = Faker()


class UIHelper:

    # os_name = platform.system()
    # CMD_CTRL = Keys.COMMAND if os_name == "darwin" else Keys.CONTROL

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.actions = ActionChains(self.driver)
        self.fake = Faker()


    def open(self):
        self.driver.get(self._PAGE_URL)

    def is_opened(self):
        self.wait.until(EC.url_to_be(self._PAGE_URL))

    def find(self, locator: tuple, message: str = "", wait: bool = False) -> WebElement:
        """
        This method finds an element with waits
        :param locator: Tuple (using in metaclasses)
        :param message: Error message if element was not found
        :param wait: Use waits or just find_element
        :return: WebElement
        """
        if wait:
            element = self.wait.until(EC.visibility_of_element_located(locator), message=message)
        else:
            element = self.driver.find_element(*locator)
        return element

    def find_all(self, locator: tuple, message: str = "", wait: bool = True) -> list[WebElement]:
        if wait:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator), message=message)
        else:
            elements = self.driver.find_elements(*locator)
        return elements

    def fill(self, locator: tuple, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator: tuple, message: str = ""):
        self.wait.until(EC.element_to_be_clickable(locator), message=message).click()

    def screenshot(self, name: str = "screenshot"):
        # Создаём имя: название_теста_2023-10-27_15-30-05
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = f"{name}_{timestamp}"
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

    def wait_for_invisibility(self, locator: tuple, message: str = "") -> WebElement:
        element = self.wait.until(EC.invisibility_of_element_located(locator), message=message)
        return element

    def wait_for_visibility(self, locator: tuple, message: str = "") -> WebElement:
        element = self.wait.until(EC.visibility_of_element_located(locator), message=message)
        return element

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

    def click_js(self, locator: tuple):
        # JS-клик
        element = self.find(locator, wait=True)
        self.driver.execute_script("arguments[0].click();", element)


