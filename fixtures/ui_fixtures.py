import os
import datetime
from dotenv import load_dotenv
import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.mail_helper import EmailHelper
from pages.login_page.page import LoginPage

def _get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # МАГИЯ: Локально браузер будет открываться визуально, а в GitHub Actions — в скрытом headless режиме!
    if os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options

@pytest.fixture(autouse=True, scope="function")
def driver(request):
    # Опции
    options = _get_chrome_options()
    # Активация headless режима
    #options.add_argument("--headless=new")
    # Необходимы для Linux/Docker в CI/CD
    remote_url = os.getenv("SELENIUM_REMOTE_URL")

    if remote_url:
        # Запуск в Docker через Selenium Grid
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        # Запуск локально (как раньше)
        driver = webdriver.Chrome(options=options)

    request.cls.driver = driver
    yield driver  # Передается управление тесту
    driver.quit()

# Вариант с использованием двух браузеров
def get_driver():
    driver_name = os.environ.get("BROWSER", "chrome").strip().lower()  # "chrome" по умолчанию
    driver = None
    if driver_name == "chrome":
        options = _get_chrome_options()
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


# @pytest.fixture # вариант с залогиненым пользователем
# def logged_admin(driver):
#     page = LoginPage(driver)
#     page.login(Credentials.ADMIN_LOGIN, Credentials.ADMIN_PASSWORD)
#     return page # Возвращаем уже залогиненную страницу


def _get_authenticated_driver(user_role: str):
    """
    Поднимает браузер и проверяет куки.
    Если куки протухли на сервере — удаляет файл и регается/логинится заново.
    """

    driver = get_driver()
    login_page = LoginPage(driver)
    cookies_file = f"cookies_{user_role}.json"

    # Шаг 1: Если файла нет — чистый UI вход
    if not os.path.exists(cookies_file):
        _perform_ui_login_flow(login_page, user_role, cookies_file)
        return driver

    # Шаг 2: Файл есть, пробуем подкинуть
    print(f"\n[Session] Найдена старая сессия для '{user_role}'. Применяю куки...")
    login_page.open()
    login_page.load_cookies(cookies_file)
    driver.refresh()

    # Шаг 3: Проверяем, сработал ли вход на самом деле
    try:
        # Если мы залогинились, кнопки логина (или поля ввода) НЕ должно быть на экране.
        # Ставим маленький таймаут в 3 секунды, чтобы тест не висел.
        # Ипользуем локатор поля логина из login_page
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(login_page._LOGIN_FIELD)
        )
        # Если мы попали сюда — значит, поле логина ВИДНО. Куки отвергнуты сервером!
        print(f"[Session] Предупреждение: Сервер отклонил куки для '{user_role}' (база очищена).")
        try:
            os.remove(cookies_file)
        except OSError:
            pass
        _perform_ui_login_flow(login_page, user_role, cookies_file)

    except:
        # Если упали в except — значит поле логина НЕ появилось (мы успешно вошли на Home)
        print(f"[Session] Отлично! Сессия для '{user_role}' подтверждена сервером.")

    return driver


def _perform_ui_login_flow(login_page, user_role, cookies_file):
    """Чистый вход через UI и сохранение свежих кук"""
    login_page.open()
    login_page.is_opened()
    login_page.login_as(user_role)
    login_page.save_cookies(cookies_file)
    print(f"[Session] Созданы свежие куки для '{user_role}' через UI-логин.")


@pytest.fixture
def admin_browser():
    driver = _get_authenticated_driver("admin")
    yield driver
    driver.quit()

@pytest.fixture
def friend_browser():
    driver = _get_authenticated_driver("friend")
    yield driver
    driver.quit()


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






