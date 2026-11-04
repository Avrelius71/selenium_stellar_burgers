from pages.base_page import BasePage


class LoginPage(BasePage):
    _path = "/login"
    _email_input = ("xpath", "(//input[@type='text'])[1]")
    _password_input = ("xpath", "//input[@type='password']")
    _submit_button = ("xpath", "//button[text()='Войти']")
    _reset_password_button = ("xpath", "//a[text()='Восстановить пароль']")

    def open_login_page(self) -> None:
        """Открыть страницу авторизации."""
        self.open(self._path)

    def input_email_log(self, email: str) -> None:
        """Ввести email в форму авторизации."""
        self.input_text(locator=self._email_input, text=email)

    def input_password_log(self, password: str) -> None:
        """Ввести пароль в форму авторизации."""
        self.input_text(locator=self._password_input, text=password)

    def submit_login(self) -> None:
        """Нажать кнопку «Войти»."""
        self.click_element(self._submit_button)

    def check_authorization(self) -> None:
        """Проверить успешную авторизацию и редирект на главную."""
        url = f"{self.base_url}/"
        self.check_url(url)
        assert self.driver.current_url == url, (
            f"Ожидались на {url}, но URL: {self.driver.current_url}"
        )

    def click_reset_button(self) -> None:
        """Нажать ссылку «Восстановить пароль»."""
        self.click_element(self._reset_password_button)
