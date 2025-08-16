import time
import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (TimeoutException,
                                        ElementClickInterceptedException)
from selenium.webdriver.common.action_chains import ActionChains
from pages.MainPage import MainPage
from config import BASE_URL
from pages.LoginPage import LoginPage


@allure.feature("UI: Вход и регистрация")
class TestLoginUI:
    @allure.story("Валидный номер и активация кнопки")
    @allure.description(
        "Проверяет, что при вводе валидного номера кнопка "
        "'Получить код' становится активной."
    )
    def test_valid_phone_number_activates_button(self,
                                                 driver: WebDriver):
        with allure.step("# 1. Главная страница"):
            mp = MainPage(driver)
            driver.get(BASE_URL)
            mp.check_main_page_elements()
        assert mp.is_main_page_displayed(), "Гл. стр. не отобразилась"

    def test_2(self, driver: WebDriver):
        valid_phone_number = "+79166192571"

        main_page = MainPage(driver)
        driver.get(BASE_URL)
        main_page.check_main_page_elements()

        main_page.go_to_login_page()

        login_page = LoginPage(driver)

        login_page.enter_phone_number(valid_phone_number)

        actual_phone = login_page.get_phone_number()
        assert actual_phone == "+7 (916) 619-25-71", (
            "Введенный номер не соответствует ожидаемому. "
            f"Ожидался: {valid_phone_number}, получен: "
            f"{actual_phone}")

        assert login_page.is_get_code_button_enabled(), (
            "Кнопка 'Получить код' не активировалась при "
            "валидном номере.")


@allure.feature("UI: Основные элементы главной страницы")
class TestMainPageUI:
    @allure.story("Проверка открытия корзины")
    @allure.description(
        "Проверяет, что при клике на иконку корзины "
        "открывается страница корзины."
    )
    def test_open_cart(self, driver: WebDriver):
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            driver.get(BASE_URL)
            main_page.check_main_page_elements()

        with allure.step("Открытие корзины"):
            main_page.open_cart()

        with allure.step("Проверка открытия страницы корзины"):
            CART_PAGE_LOCATOR = (By.XPATH,
                                 "//h1[contains(text(), 'Корзина')]")
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        CART_PAGE_LOCATOR
                    )
                )
            except TimeoutException:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                raise AssertionError(
                    "Страница корзины не открылась. "
                    "Элемент не найден."
                )


logging.basicConfig(level=logging.INFO)


@allure.feature("UI: Поиск")
@allure.story("Книга и страница")
@allure.description("Поиск, переход.")
@pytest.mark.parametrize("title", ["Мастер и Маргарита"])
def test_search_book_and_open_product_page(driver: WebDriver, title: str):
    with allure.step(f"Проверка, что книга '{title}' найдена и открыта"):
        with allure.step("# 1. Главная страница"):
            mp = MainPage(driver)
            driver.get(BASE_URL)
            mp.check_main_page_elements()
        assert mp.is_main_page_displayed(), "Гл. стр. не отобразилась"

        with allure.step(f"# 2. Поиск: {title}"):
            mp.search(title)

        with allure.step("# 3. Находим, переходим"):
            try:
                xpath_class = '//a[@class="product-card__title"'
                xpath_href = ' and contains(@href, \
                    "/product/master-i-margarita")'
                xpath_text = ' and contains(text(), \
                    "Мастер и Маргарита")]'
                locator = (
                    By.XPATH,
                    xpath_class + xpath_href + xpath_text
                )

                first_result_link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(locator)
                )

                scroll_script = \
                    "arguments[0].scrollIntoView({block: 'center'});"
                driver.execute_script(scroll_script, first_result_link)

                time.sleep(0.5)

                # --- Повторно находим элемент перед кликом ---
                first_result_link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(locator)
                )

                actions = ActionChains(driver)
                actions.move_to_element(first_result_link).click().perform()

                WebDriverWait(driver, 15).until(
                    lambda driver: driver.current_url != BASE_URL)

            except TimeoutException:
                allure.attach(driver.get_screenshot_as_png(),
                              name="search_results_timeout",
                              attachment_type=allure.attachment_type.PNG)
                logging.error("Не дождались")
                logging.error(f"HTML: {driver.page_source}")
                assert False, "Не дождались"
            except ElementClickInterceptedException:
                allure.attach(driver.get_screenshot_as_png(),
                              name="element_intercepted",
                              attachment_type=allure.attachment_type.PNG)
                logging.error("Элемент перекрыт")
                assert False, "Элемент перекрыт"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="search_results_error",
                              attachment_type=allure.attachment_type.PNG)
                logging.exception(f"Ошибка: {e}")
                assert False, f"Ошибка: {e}"

        with allure.step("# 4. Проверяем страницу товара"):
            try:
                title_locator = (By.CLASS_NAME,
                                 "product-detail-page__title")
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(title_locator))
                title_text = driver.find_element(*title_locator).text.lower()

                assert title.lower() in title_text, \
                    f"Нет книги: {title}"
            except TimeoutException:
                allure.attach(driver.get_screenshot_as_png(),
                              name="prod_page_timeout",
                              attachment_type=allure.attachment_type.PNG)
                logging.error("Нет страницы товара")
                assert False, "Нет страницы товара"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="prod_page_error",
                              attachment_type=allure.attachment_type.PNG)
                logging.exception(f"Ошибка: {e}")
                assert False, f"Ошибка: {e}"


@allure.story("тест главной страницы")
def test_main_page_simplest(driver: WebDriver):
    with allure.step("Открываем главную страницу и проверяем заголовок"):
        try:
            driver.get("https://www.chitai-gorod.ru/")

            allure.attach(driver.get_screenshot_as_png(),
                          name="main_page",
                          attachment_type=allure.attachment_type.PNG)

            assert driver.title != "", "Title страницы пустой!"

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(),
                          name="main_page_error",
                          attachment_type=allure.attachment_type.PNG)
            assert False, f"Ошибка: {e}"