import os
from dotenv import load_dotenv

load_dotenv()


class Credentials:

    FRIEND_LOGIN = os.getenv("FRIEND_LOGIN")
    FRIEND_PASSWORD = os.getenv("FRIEND_PASSWORD")
    FRIEND_EMAIL = os.getenv("FRIEND_EMAIL")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")