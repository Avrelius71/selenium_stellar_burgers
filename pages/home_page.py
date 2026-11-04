from pages.base_page import BasePage, Locator


class HomePage(BasePage):
    _button_login_ac = ("xpath", "//*[text()='Войти в аккаунт']")
    _button_personal_account = ("xpath", "//*[text()='Личный Кабинет']")
    _link_profile = ("xpath", "//*[text()='Профиль']")
    _link_constructor = ("xpath", "//*[text()='Конструктор']")
    _stellar_link = ("xpath", "//div[contains(@class, 'header__logo')]//a")
    _logout_loc = ("xpath", "//*[text()='Выход']")
    _tab_buns = ("xpath", "//span[text()='Булки']/..")
    _tab_sauces = ("xpath", "//span[text()='Соусы']/..")
    _tab_fillings = ("xpath", "//span[text()='Начинки']/..")

    def click_button_login_account(self) -> None:
        """Нажать кнопку «Войти в аккаунт»."""
        self.click_element(self._button_login_ac)

    def click_button_personal_account(self) -> None:
        """Нажать кнопку «Личный кабинет»."""
        self.click_element(self._button_personal_account)

    def click_link_constructor(self) -> None:
        """Нажать ссылку «Конструктор» в шапке."""
        self.click_element(self._link_constructor)

    def click_link_stellar(self) -> None:
        """Нажать логотип Stellar Burgers в шапке."""
        self.click_element(self._stellar_link)

    def click_logout_profile(self) -> None:
        """Нажать кнопку «Выход» в личном кабинете."""
        self.click_element(self._logout_loc)

    def click_tab_buns(self) -> None:
        """Перейти на вкладку «Булки»."""
        self.click_element(self._tab_buns)

    def click_tab_sauces(self) -> None:
        """Перейти на вкладку «Соусы»."""
        self.click_element(self._tab_sauces)

    def click_tab_fillings(self) -> None:
        """Перейти на вкладку «Начинки»."""
        self.click_element(self._tab_fillings)

    def check_personal_account(self) -> None:
        """Проверить переход в личный кабинет."""
        text = self.find_element(self._link_profile).text
        assert text == "Профиль", f"Ожидался текст «Профиль», получено: {text}"
        expected_url = f"{self.base_url}/account/profile"
        assert self.driver.current_url == expected_url, (
            f"Ожидался URL {expected_url}, получен: {self.driver.current_url}"
        )

    def check_redirect_base_url(self) -> None:
        """Проверить редирект на главную страницу."""
        url = f"{self.base_url}/"
        self.check_url(url)

    def check_logout(self) -> None:
        """Проверить выход из аккаунта и редирект на страницу авторизации."""
        url = f"{self.base_url}/login"
        self.check_url(url)
        assert self.driver.current_url == url, (
            f"Ожидался URL {url}, получен: {self.driver.current_url}"
        )

    def _check_tab_active(self, tab_locator: Locator) -> None:
        """Проверить, что вкладка конструктора активна."""
        self.wait.until(
            lambda driver: "current" in driver.find_element(*tab_locator).get_attribute("class")
        )

    def check_buns_tab_active(self) -> None:
        """Проверить, что активна вкладка «Булки»."""
        self._check_tab_active(self._tab_buns)

    def check_sauces_tab_active(self) -> None:
        """Проверить, что активна вкладка «Соусы»."""
        self._check_tab_active(self._tab_sauces)

    def check_fillings_tab_active(self) -> None:
        """Проверить, что активна вкладка «Начинки»."""
        self._check_tab_active(self._tab_fillings)
