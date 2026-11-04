from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
import allure

from config.environments import EnvironmentConfig

Locator = tuple[str, str]


class BasePage:
    """Базовый класс для всех страниц"""
    _modal_overlay = (By.CSS_SELECTOR, "[class*=\"Modal_modal_overlay\"]")

    def __init__(self, driver: WebDriver, env_config: EnvironmentConfig) -> None:
        self.driver = driver
        self.base_url = env_config.url.rstrip("/")
        self.wait = WebDriverWait(driver, env_config.timeout)

    def _wait_for_page_ready(self) -> None:
        """Дождаться исчезновения модального оверлея после загрузки страницы."""
        self.wait.until(
            lambda driver: not any(
                overlay.is_displayed()
                for overlay in driver.find_elements(*self._modal_overlay)
            )
        )

    def open(self, path: str = "") -> None:
        """Открыть страницу: base_url или base_url + путь."""
        if path:
            url = f"{self.base_url}/{path.lstrip('/')}"
        else:
            url = self.base_url
        self.driver.get(url)
        self._wait_for_page_ready()

    def find_element(self, locator: Locator) -> WebElement:
        """Найти элемент с явным ожиданием."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator: Locator) -> None:
        """Нажать на элемент с явным ожиданием кликабельности."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator: Locator, text: str) -> None:
        """Ввести текст в элемент."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def check_url(self, url: str) -> None:
        """Дождаться перехода на указанный URL."""
        self.wait.until(EC.url_to_be(url))

    def attach_screenshot(self, name: str = "screenshot") -> None:
        """Сделать скриншот и прикрепить к отчету Allure."""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
