import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.skip
@pytest.mark.regression
@allure.feature("Навигация")
class TestNavigation:

    @allure.title("Переход в личный кабинет")
    @pytest.mark.smoke
    def test_personal_account(
        self,
        create_account: tuple[str, str],
        home_page: HomePage,
        login_page: LoginPage,
    ) -> None:
        email, password = create_account
        with allure.step("Открываем главную страницу и переходим к авторизации"):
            home_page.open()
            home_page.click_button_personal_account()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(email)
            login_page.input_password_log(password)
            login_page.submit_login()
        with allure.step("Проверяем переход в личный кабинет"):
            home_page.click_button_personal_account()
            home_page.check_personal_account()

    @allure.title("Переход по клику на кнопку 'Конструктор'")
    def test_navigation_constructor(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()
        with allure.step("Переходим на страницу авторизации через «Личный кабинет»"):
            home_page.click_button_personal_account()
        with allure.step("Переходим на главную через «Конструктор»"):
            home_page.click_link_constructor()
            home_page.check_redirect_base_url()

    @allure.title("Переход по клику на кнопку 'Stellar Burgers'")
    def test_navigation_stellar_burgers(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()
        with allure.step("Переходим на страницу авторизации через «Личный кабинет»"):
            home_page.click_button_personal_account()
        with allure.step("Переходим на главную через логотип Stellar Burgers"):
            home_page.click_link_stellar()
            home_page.check_redirect_base_url()

    @allure.title("Проверка выхода из личного кабинета")
    @pytest.mark.smoke
    def test_logout_personal_account(
        self,
        create_account: tuple[str, str],
        home_page: HomePage,
        login_page: LoginPage,
    ) -> None:
        email, password = create_account
        with allure.step("Открываем главную страницу и переходим к авторизации"):
            home_page.open()
            home_page.click_button_personal_account()
        with allure.step("Выполняем авторизацию"):
            login_page.input_email_log(email)
            login_page.input_password_log(password)
            login_page.submit_login()
        with allure.step("Проверяем выход из личного кабинета"):
            home_page.click_button_personal_account()
            home_page.click_logout_profile()
            home_page.check_logout()

    @allure.title("Проверка перехода к разделу 'Булки'")
    def test_navigation_buns(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()
        with allure.step("Переходим в раздел «Соусы»"):
            home_page.click_tab_sauces()
        with allure.step("Переходим в раздел «Булки» и проверяем активную вкладку"):
            home_page.click_tab_buns()
            home_page.check_buns_tab_active()

    @allure.title("Проверка перехода к разделу 'Соусы'")
    def test_navigation_sauces(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()
        with allure.step("Переходим в раздел «Соусы» и проверяем активную вкладку"):
            home_page.click_tab_sauces()
            home_page.check_sauces_tab_active()

    @allure.title("Проверка перехода к разделу 'Начинки'")
    def test_navigation_fillings(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()
        with allure.step("Переходим в раздел «Начинки» и проверяем активную вкладку"):
            home_page.click_tab_fillings()
            home_page.check_fillings_tab_active()
