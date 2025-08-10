import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
import allure
from pages.MainPage import MainPage
from pages.LoginPage import LoginPage
from config import BASE_URL

@pytest.mark.ui
@allure.feature("UI: Вход и регистрация")
class TestLoginUI:

    @allure.story("Валидный номер и активация кнопки")
    @allure.description(
        "Проверяет, что при вводе валидного номера кнопка "
        "'Получить код' становится активной."
    )
    def test_valid_phone_number_activates_button(
            self, driver: WebDriver
    ):
        """Проверяет активацию кнопки при вводе валидного номера."""
        valid_phone_number = "+79166192571"

        # 1. Переходим на главную страницу
        main_page = MainPage(driver)
        driver.get(BASE_URL)  # Явно переходим по URL
        assert main_page.is_main_page_displayed(), (
            "Главная страница не отобразилась. Проверьте "
            "BASE_URL в config.py и локаторы."
        )

        # 2. Открываем модальное окно входа
        main_page.go_to_login_page()

        # 3. Создаем экземпляр LoginPage
        login_page = LoginPage(driver)

        # 4. Вводим валидный номер
        login_page.enter_phone_number(valid_phone_number)

        # 5. Проверяем, что введенный номер соответствует
        actual_phone = login_page.get_phone_number()
        assert actual_phone == valid_phone_number, (
            "Введенный номер не соответствует ожидаемому. "
            f"Ожидался: {valid_phone_number}, получен: "
            f"{actual_phone}"
        )

        # 6. Проверяем, что кнопка стала активной
        assert login_page.is_get_code_button_enabled(), (
            "Кнопка 'Получить код' не активировалась при "
            "валидном номере."
        )
