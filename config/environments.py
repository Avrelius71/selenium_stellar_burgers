from dataclasses import dataclass
from enum import Enum


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
    "user1": UserCredentials("test17@ya.ru", "Gfhjkm<ehuth"),
    "user2": UserCredentials("AQA17@ya.ru", "Gfhjkm:jgf")
}


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
