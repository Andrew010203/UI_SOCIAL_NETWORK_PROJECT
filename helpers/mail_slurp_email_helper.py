import os
import re
from mailslurp_client import Configuration, ApiClient, InboxControllerApi, WaitForControllerApi
from dotenv import load_dotenv


class MailSlurpEmailHelper:
    def __init__(self, api_key: str):
        config = Configuration()
        config.api_key["x-api-key"] = api_key
        self.client = ApiClient(config)
        self.client.rest_client.pool_manager.connection_pool_kw['timeout'] = 10
        self.inbox_api = InboxControllerApi(self.client)
        self.wait_api = WaitForControllerApi(self.client)

    def create_inbox(self) -> dict:
        inbox = self.inbox_api.create_inbox()
        return {"id": inbox.id, "email": inbox.email_address}

    def wait_for_email(self, inbox_id: str, timeout_ms: int = 60000) -> dict:
        email = self.wait_api.wait_for_latest_email(inbox_id=inbox_id, timeout=timeout_ms)
        return {"subject": email.subject, "body": email.body}

    def get_link(self, body: str, keyword: str = "verify") -> str:
        r"""
        Ищет URL, содержащий конкретное ключевое слово (activate, verify, confirm).
        [^\s<>"]+ — исключает пробелы, кавычки и скобки, которые могут окружать URL в HTML.
        """
        pattern = rf'https?://[^\s<>"]+{keyword}[^\s<>"]+'
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group() if match else None


    # def get_link(self, body: str, domain: str = "://openteknik.com") -> str:
    #     """
    #     Ищет первую попавшуюся ссылку, которая ведет на домен.
    #     Экранируем точки в домене для корректной работы regex.
    #     """
    #     escaped_domain = domain.replace(".", r"\.")
    #     pattern = rf'https?://{escaped_domain}[^\s<>"]+'
    #     match = re.search(pattern, body)
    #     return match.group() if match else None

    def close(self):
        self.client.__exit__(None, None, None)