from collections.abc import Generator
import os

import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.environments import (
    Environment,
    EnvironmentConfig,
    UserCredentials,
    common_users,
    environments,
    print_environment_info,
)
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.reset_password_page import ResetPasswordPage


fake = Faker("en_US")

DEVICE_PRESETS = {
    "mobile": (375, 667),
    "tablet": (768, 1024),
    "laptop": (1024, 768),
    "desktop": (1280, 800)
}

COHORT = "17"
DOMAIN = "yandex.ru"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        default=os.getenv("BROWSER", "chrome"),
        help="chrome/firefox (или переменная окружения BROWSER)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="headless-режим (или HEADLESS=true в окружении)",
    )
    parser.addoption("--device", default=None, help="mobile/tablet/laptop/desktop")
    parser.addoption("--env", default="dev", help="dev/stage")
    parser.addoption("--user-type", default=None)


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def create_driver(browser: str, headless: bool, width: int, height: int) -> WebDriver:
    if browser == "chrome":
        options = ChromeOptions()
        chrome_bin = os.getenv("CHROME_BIN")
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
        if chrome_bin:
            options.binary_location = chrome_bin
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
        if chromedriver_path:
            return webdriver.Chrome(
                service=ChromeService(chromedriver_path),
                options=options,
            )
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(width, height)
        return driver
    else:
        raise ValueError(f"Browser {browser} not supported")


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or _env_flag("HEADLESS")
    device = request.config.getoption("--device")
    width, height = DEVICE_PRESETS.get(device, (1280, 800))
    driver = create_driver(browser, headless, width, height)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)


def pytest_configure(config: pytest.Config) -> None:
    env_name = config.getoption("--env")
    user_type = config.getoption("--user-type")
    print_environment_info(env_name, user_type)


@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    env_name = request.config.getoption("--env")
    return environments[Environment(env_name)]


@pytest.fixture(scope="function")
def user(request: pytest.FixtureRequest, env_config: EnvironmentConfig) -> UserCredentials:
    user_type = request.config.getoption("--user-type") or env_config.default_user
    return common_users[user_type]


@pytest.fixture
def registr_page(driver: WebDriver, env_config: EnvironmentConfig) -> RegistrationPage:
    return RegistrationPage(driver, env_config)


@pytest.fixture
def login_page(driver: WebDriver, env_config: EnvironmentConfig) -> LoginPage:
    return LoginPage(driver, env_config)


@pytest.fixture
def home_page(driver: WebDriver, env_config: EnvironmentConfig) -> HomePage:
    return HomePage(driver, env_config)


@pytest.fixture
def reset_page(driver: WebDriver, env_config: EnvironmentConfig) -> ResetPasswordPage:
    return ResetPasswordPage(driver, env_config)


def generate_email() -> str:
    return (
        f"{fake.first_name().lower()}"
        f"{fake.last_name().lower()}"
        f"{COHORT}"
        f"{fake.numerify('###')}"
        f"@{DOMAIN}"
    )


@pytest.fixture
def create_account(registr_page: RegistrationPage) -> Generator[tuple[str, str], None, None]:
    name = fake.first_name()
    email = generate_email()
    password = fake.password(length=10)
    registr_page.open_registration_page()
    registr_page.input_name_reg(name)
    registr_page.input_email_reg(email)
    registr_page.input_password_reg(password)
    registr_page.confirm_reg()
    registr_page.check_registration_success()
    yield email, password
