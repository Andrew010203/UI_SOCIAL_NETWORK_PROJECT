import os
import datetime
from dotenv import load_dotenv
import allure
import pytest
import requests
from selenium import webdriver

from helpers.mail_slurp_email_helper import MailSlurpEmailHelper
from pages.login_page.page import LoginPage


@pytest.fixture(autouse=True, scope="function")
def driver(request):
    # Опции
    options = webdriver.ChromeOptions()
    options.browser_version = "stable"
    options.add_argument("--window-size=1920,1080")
    # Активация headless режима
    options.add_argument("--headless=new")
    # Необходимы для Linux/Docker в CI/CD
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    remote_url = os.getenv("SELENIUM_REMOTE_URL")

    if remote_url:
        # Запуск в Docker через Selenium Grid
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        # Запуск локально (как раньше)
        driver = webdriver.Chrome(options=options)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # Дополнительные опции для обхода некоторых детекторов автоматизации
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    request.cls.driver = driver
    yield driver  # Передается управление тесту
    driver.quit()

# Вариант с использованием двух браузеров
def get_driver():
    # driver = os.environ.get("BROWSER").strip().lower()
    driver_name = os.environ.get("BROWSER", "chrome").strip().lower()  # "chrome" по умолчанию
    driver = None
    if driver_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        # Дополнительные опции для обхода некоторых детекторов автоматизации
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
    elif driver_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--disable-search-engine-choice-screen")
        driver = webdriver.Firefox(options=options)
    if driver is None:
        raise ValueError(f"Unsupported browser: {driver_name}")
    return driver


@pytest.fixture  # вместо add_users отдельный экземпляр конкретного юзера
def admin(request):
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture  # вместо add_users отдельный экземпляр конкретного юзера
def friend(request):
    driver = get_driver()
    yield driver
    driver.quit()

# @pytest.fixture # вариант с залогиненым пользователем
# def logged_admin(driver):
#     page = LoginPage(driver)
#     page.login(Credentials.ADMIN_LOGIN, Credentials.ADMIN_PASSWORD)
#     return page # Возвращаем уже залогиненную страницу

@pytest.fixture
def setup_session(driver):
    login_page = LoginPage(driver)
    cookies_file = "cookies.json"

    # Проверяем, существует ли файл физически на диске
    if not os.path.exists(cookies_file):
        login_page.open()
        login_page.is_opened()
        login_page.login_as("friend")
        login_page.save_cookies(cookies_file)
        # Добавим принт для логов, чтобы видеть в терминале, что был UI-логин
        print("\n[Session] Cookie file created via UI login.")
    else:
        # Сначала открываем домен, чтобы Selenium позволил подкинуть куки
        login_page.open()
        login_page.is_opened()
        login_page.load_cookies(cookies_file)
        print("\n[Session] Login performed via cookies.")



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Этот хук выполняется на каждом этапе теста (setup, call, teardown)
    outcome = yield
    rep = outcome.get_result()

    # Мы проверяем, что это этап вызова теста (call) и он завершился неудачей
    if rep.when == 'call' and rep.failed:
        try:
            # Пытаемся достать драйвер из тестового класса
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
            elif hasattr(item.instance, 'driver'):
                driver = item.instance.driver
            else:
                return

            # Делаем скриншот и крепим к Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot_On_Failure_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Fail to take screenshot: {e}")


@pytest.fixture(scope="function")
def email_helper():
    # Достаем токен один раз здесь
    token = os.getenv("EMAIL_API_TOKEN")
    # Передаем его в конструктор класса
    helper = MailSlurpEmailHelper(api_key=token)
    yield helper
    helper.close()


# @pytest.fixture(scope="function")
# def email_helper():
#     # Инициализируем хелпер, используя токен из .env
#     token = os.getenv("EMAIL_API_TOKEN")
#     if not token:
#         pytest.skip("EMAIL_API_TOKEN not found in environment variables")
#
#     helper = MailSlurpEmailHelper(token)
#     yield helper
#     # Метод close() гарантирует, что соединение с MailSlurp будет разорвано корректно
#     helper.close()

