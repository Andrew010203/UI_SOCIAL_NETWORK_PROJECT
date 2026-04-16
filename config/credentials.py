import os
from dotenv import load_dotenv

load_dotenv()

class Credentials:

    # FakeWorld123
    FRIEND_LOGIN = os.getenv("FRIEND_LOGIN")
    FRIEND_PASSWORD = os.getenv("FRIEND_PASSWORD")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")