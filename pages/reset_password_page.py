from pages.base_page import BasePage


class ResetPasswordPage(BasePage):

    _login_button = ("xpath", "//a[text()='Войти']")

    def click_login_button(self) -> None:
        """Нажать ссылку «Войти» на странице восстановления пароля."""
        self.click_element(self._login_button)
