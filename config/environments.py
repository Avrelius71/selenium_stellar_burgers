import os
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv


# Загружаем переменные из файла .env (если он существует)
load_dotenv()


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {"dev": "Dev", "stage": "Stage"}[self]


@dataclass
class UserCredentials:
    username: str
    password: str


# Общие пользователи, доступные для всех окружений
common_users = {
    "user1": UserCredentials(
        username=os.getenv("USER1_EMAIL", "default_user1@example.com"),
        password=os.getenv("USER1_PASSWORD", "default_password")
    ),
    "user2": UserCredentials(
        username=os.getenv("USER2_EMAIL", "default_user2@example.com"),
        password=os.getenv("USER2_PASSWORD", "default_password")
    )
}

if "default_password" in [common_users["user1"].password, common_users["user2"].password]:
    print("WARNING: Тестовые пароли не найдены в .env файле! Используются значения по умолчанию.")


@dataclass
class EnvironmentConfig:
    url: str
    timeout: int
    default_user: str

    def __str__(self):
        return f"- URL: {self.url}"

dev_url = "https://stellarburgers.education-services.ru"
stage_url = "https://stellarburgers.education-services.ru"

environments = {
    Environment.DEV: EnvironmentConfig(dev_url, 15, "user1"),
    Environment.STAGE: EnvironmentConfig(stage_url, 10, "user2")
}


def print_environment_info(env_name, user_type=None):
    """Вывод информации о тестовом окружении."""
    try:
        env = Environment(env_name)
        config = environments[env]
        user_type = user_type or config.default_user
        user = common_users.get(user_type)

        print(f"\nEnvironment: {env}")
        print(f"{config}")

        if user:
            print(f"- User: {user.username}")
        else:
            print(f"- User type '{user_type}' not found!")
    except (ValueError, KeyError):
        print(f"Environment '{env_name}' not found!")
