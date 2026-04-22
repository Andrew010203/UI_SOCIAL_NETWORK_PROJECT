import time

import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials


class HomePage(BasePage):

    _PAGE_URL = Links.HOME_PAGE