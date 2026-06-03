import os
import re
from mailslurp_client import Configuration, ApiClient, InboxControllerApi, WaitForControllerApi
from dotenv import load_dotenv


class EmailHelper:
    """
    Хелпер для интеграции с API сервиса MailSlurp.
    Используется для генерации динамических почтовых ящиков и валидации писем.
    """
    def __init__(self, api_key):
        """Инициализация клиента MailSlurp API и контроллеров ожидания"""
        config = Configuration()
        config.api_key["x-api-key"] = api_key
        self.client = ApiClient(config)
        self.client.rest_client.pool_manager.connection_pool_kw['timeout'] = 10
        self.inbox_api = InboxControllerApi(self.client)
        self.wait_api = WaitForControllerApi(self.client)

    def create_inbox(self) -> dict:
        """
        Создает новый временный почтовый ящик.
        :return: Словарь с ID и полным email-адресом созданного ящика
        """
        # _request_timeout=15 страхует от вечного зависания при сетевых сбоях
        inbox = self.inbox_api.create_inbox(_request_timeout=15)
        return {"id": inbox.id, "email": inbox.email_address}

    def wait_for_email(self, inbox_id: str, timeout_ms: int = 60000) -> dict:
        """
        Блокирующий метод: ожидает поступление нового письма в указанный инбокс.
        :param inbox_id: Уникальный идентификатор ящика
        :param timeout_ms: Максимальное время ожидания письма в миллисекундах
        :return: Текст темы (subject) и html/text тело сообщения (body)
        """
        email = self.wait_api.wait_for_latest_email(inbox_id=inbox_id, timeout=timeout_ms)
        return {"subject": email.subject, "body": email.body}

    def get_link(self, body: str, keyword: str = "validate") -> str:
        r"""
        Парсит тело письма и извлекает URL-ссылку, содержащую ключевое слово.
        [^\s<>"]+ — исключает пробелы, кавычки и скобки, окружающие ссылку в HTML.
        :param body: Текст или HTML-код письма
        :param keyword: Ключевое слово для фильтрации целевой ссылки
        """
        pattern = rf'https?://[^\s<>"]+{keyword}[^\s<>"]+'
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group() if match else None

    def close(self):
        self.client.__exit__(None, None, None)