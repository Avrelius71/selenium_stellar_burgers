from pages.base_page import BasePage
from faker import Faker


fake = Faker("en_US")


class RegistrationPage(BasePage):
    _path = "/register"
    _name_input = ("xpath", "(//input[@type='text'])[1]")
    _email_input = ("xpath", "(//input[@type='text'])[2]")
    _password_input = ("xpath", "//input[@type='password']")
    _submit_button = ("xpath", "//button[text()='Зарегистрироваться']")
    _after_reg_url = "/login"
    _login_heading = ("xpath", "//h2[text()='Вход']")
    _error_loc = ("xpath", "//*[text()='Некорректный пароль']")
    _button_login_account = ("xpath", "//a[text()='Войти']")

    def open_registration_page(self) -> None:
        """Открыть страницу регистрации."""
        self.open(self._path)

    def input_name_reg(self, name: str | None = None) -> None:
        """Ввести имя в форму регистрации."""
        if name is None:
            self.input_text(locator=self._name_input, text=fake.first_name())
        else:
            self.input_text(locator=self._name_input, text=name)

    def input_email_reg(self, email: str | None = None) -> None:
        """Ввести email в форму регистрации."""
        if email is None:
            email = (
                f"{fake.first_name().lower()}"
                f"{fake.last_name().lower()}"
                f"17"
                f"{fake.numerify('###')}"
                f"@yandex.ru"
            )
        self.input_text(locator=self._email_input, text=email)

    def input_password_reg(self, password: str | None = None) -> None:
        """Ввести пароль в форму регистрации."""
        if password is None:
            self.input_text(locator=self._password_input, text=fake.password(length=10))
        else:
            self.input_text(locator=self._password_input, text=password)

    def confirm_reg(self) -> None:
        """Нажать кнопку «Зарегистрироваться»."""
        self.click_element(self._submit_button)

    def check_registration_success(self) -> None:
        """Проверить успешную регистрацию и редирект на страницу авторизации."""
        auth_url = f"{self.base_url}{self._after_reg_url}"
        self.check_url(auth_url)
        self.find_element(self._login_heading)

    def check_not_registration(self) -> None:
        """Проверить, что регистрация не прошла и URL не изменился."""
        reg_url = f"{self.base_url}{self._path}"
        self.check_url(reg_url)
        assert self.driver.current_url == reg_url, (
            f"Ожидались на {reg_url}, но URL: {self.driver.current_url}"
        )

    def check_error(self) -> None:
        """Проверить отображение ошибки «Некорректный пароль»."""
        text_error = self.find_element(self._error_loc).text
        assert text_error == "Некорректный пароль", (
            f"Ожидалось сообщение «Некорректный пароль», получено: {text_error}"
        )

    def click_login_acc(self) -> None:
        """Нажать ссылку «Войти» на странице регистрации."""
        self.click_element(self._button_login_account)
