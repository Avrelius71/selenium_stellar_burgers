import allure
import pytest

from pages.registration_page import RegistrationPage


@pytest.mark.skip
@pytest.mark.regression
@allure.feature("Регистрация аккаунта")
class TestRegistration:

    @pytest.mark.smoke
    @allure.title("Регистрация с валидными данными")
    def test_registration(self, registr_page: RegistrationPage) -> None:
        with allure.step("Заполняем форму регистрации"):
            registr_page.open_registration_page()
            registr_page.input_name_reg()
            registr_page.input_email_reg()
            registr_page.input_password_reg()
        with allure.step("Жмем кнопку \"Зарегистрировать\""):
            registr_page.confirm_reg()
        with allure.step("Проверяем редирект на страницу авторизации"):
            registr_page.check_registration_success()

    @allure.title("Регистрация с пустыми полем 'Имя'")
    def test_registration_not_name(self, registr_page: RegistrationPage) -> None:
        with allure.step("Заполняем форму регистрации"):
            registr_page.open_registration_page()
            registr_page.input_name_reg("")
            registr_page.input_email_reg()
            registr_page.input_password_reg()
        with allure.step("Жмем кнопку \"Зарегистрировать\""):
            registr_page.confirm_reg()
        with allure.step("Проверяем что регистрация не прошла"):
            registr_page.check_not_registration()

    @allure.title("Регистрация с невалидным Email")
    def test_registration_invalid_email(self, registr_page: RegistrationPage) -> None:
        with allure.step("Заполняем форму регистрации"):
            registr_page.open_registration_page()
            registr_page.input_name_reg()
            registr_page.input_email_reg("Gusy")
            registr_page.input_password_reg()
        with allure.step("Жмем кнопку \"Зарегистрировать\""):
            registr_page.confirm_reg()
        with allure.step("Проверяем что регистрация не прошла"):
            registr_page.check_not_registration()

    @allure.title("Регистрация с password < 6 символов")
    def test_registration_invalid_password(self, registr_page: RegistrationPage) -> None:
        with allure.step("Заполняем форму регистрации"):
            registr_page.open_registration_page()
            registr_page.input_name_reg()
            registr_page.input_email_reg()
            registr_page.input_password_reg("12345")
        with allure.step("Жмем кнопку \"Зарегистрировать\""):
            registr_page.confirm_reg()
        with allure.step("Проверяем что отображается ошибка"):
            registr_page.check_error()
