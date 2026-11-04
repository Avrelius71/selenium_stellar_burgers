import allure
import pytest

from config.environments import common_users
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.reset_password_page import ResetPasswordPage


@pytest.mark.skip
@pytest.mark.regression
@allure.feature("Авторизация")
class TestLogin:

    @allure.title("Авторизация через кнопку \"Войти в аккаунт\"")
    @pytest.mark.smoke
    @pytest.mark.parametrize("user_key", ["user1", "user2"])
    def test_login_button(
        self,
        login_page: LoginPage,
        home_page: HomePage,
        user_key: str,
    ) -> None:
        user = common_users[user_key]
        with allure.step("Открываем страницу авторизации"):
            home_page.open()
            home_page.click_button_login_account()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(user.username)
            login_page.input_password_log(user.password)
            login_page.submit_login()
        with allure.step("Проверяем что авторизация прошла успешно"):
            login_page.check_authorization()

    @allure.title("Авторизация через кнопку \"Личный кабинет\"")
    def test_login_button_personal_acc(
        self,
        login_page: LoginPage,
        home_page: HomePage,
        create_account: tuple[str, str],
    ) -> None:
        email, password = create_account
        with allure.step("Открываем страницу авторизации"):
            home_page.open()
            home_page.click_button_personal_account()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(email)
            login_page.input_password_log(password)
            login_page.submit_login()
        with allure.step("Проверяем что авторизация прошла успешно"):
            login_page.check_authorization()

    @allure.title("Авторизация через форму регистрации")
    def test_login_button_in_form_registr(
        self,
        login_page: LoginPage,
        registr_page: RegistrationPage,
        create_account: tuple[str, str],
    ) -> None:
        email, password = create_account
        with allure.step("Открываем страницу авторизации"):
            registr_page.open_registration_page()
            registr_page.click_login_acc()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(email)
            login_page.input_password_log(password)
            login_page.submit_login()
        with allure.step("Проверяем что авторизация прошла успешно"):
            login_page.check_authorization()

    @allure.title("Авторизация через форму восстановления пароля")
    def test_login_button_in_form_reset(
        self,
        login_page: LoginPage,
        reset_page: ResetPasswordPage,
        create_account: tuple[str, str],
    ) -> None:
        email, password = create_account
        with allure.step("Открываем страницу авторизации"):
            login_page.open_login_page()
            login_page.click_reset_button()
            reset_page.click_login_button()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(email)
            login_page.input_password_log(password)
            login_page.submit_login()
        with allure.step("Проверяем что авторизация прошла успешно"):
            login_page.check_authorization()
