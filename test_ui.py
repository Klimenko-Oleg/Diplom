import time
import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  # <- Import the actual webdriver
from selenium.common.exceptions import TimeoutException
from pages.MainPage import MainPage  # Page Object
from config import BASE_URL
from pages.LoginPage import LoginPage


@pytest.fixture
def driver() -> webdriver:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(50)
    return driver
# Тест 1


@allure.feature("UI: Вход и регистрация")
class TestLoginUI:

    @allure.story("Валидный номер и активация кнопки")
    @allure.description(
        "Проверяет, что при вводе валидного номера кнопка "
        "'Получить код' становится активной."
    )
    def test_valid_phone_number_activates_button(
            self, driver: webdriver
    ):

        # 1. Переходим на главную страницу
        main_page = MainPage(driver)
        driver.get(BASE_URL)  # Явно переходим по URL
        assert main_page.is_main_page_displayed(), (
            "Главная страница не отобразилась. Проверьте "
            "BASE_URL в config.py и локаторы."
        )

# Тест 2
    def test_2(self, driver):
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
        assert actual_phone == "+7 (916) 619-25-71", (
            "Введенный номер не соответствует ожидаемому. "
            f"Ожидался: {valid_phone_number}, получен: "
            f"{actual_phone}"
        )

        # 6. Проверяем, что кнопка стала активной
        assert login_page.is_get_code_button_enabled(), (
            "Кнопка 'Получить код' не активировалась при "
            "валидном номере."
        )
# Тест 3


@allure.feature("UI: Основные элементы главной страницы")
class TestMainPageUI:
    @allure.story("Проверка открытия корзины")
    @allure.description(
        "Проверяет, что при клике на иконку корзины "
        "открывается страница корзины."
    )
    def test_open_cart(self, driver: webdriver):
        # 1. Переходим на главную страницу
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            driver.get(BASE_URL)
            assert main_page.is_main_page_displayed(), (
                "Главная страница не отобразилась. "
                "Проверьте BASE_URL в config.py и локаторы."
            )

        # 2. Открываем корзину
        with allure.step("Открытие корзины"):
            main_page.open_cart()

        # 3. Проверяем, что открылась страница корзины
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

# Тест 4


logging.basicConfig(level=logging.INFO)


@allure.feature("UI: Поиск")
@allure.story("Книга и страница")
@allure.description("Поиск, переход.")
@pytest.mark.parametrize("title", ["Мастер и Маргарита"])
def test_search_book_and_open_product_page(
    driver: webdriver.Chrome,
    title: str
):
    """Поиск книги и переход."""
    with allure.step("# 1. Гл. стр."):
        mp = MainPage(driver)
        driver.get(BASE_URL)
        assert mp.is_main_page_displayed(), "Гл. не отобразилась"

    with allure.step(f"# 2. Поиск: {title}"):
        mp.search(title)

    with allure.step("# 3. Находим, переходим"):
        try:
            # Ищем ссылку внутри карточки товара, содержащую текст
            xpath_class = '//a[@class="product-card__title"'
            xpath_href = ' and contains(@href, "/product/master-i-margarita")'
            xpath_text = ' and contains(text(), "Мастер и Маргарита")]'
            locator = (
                By.XPATH,
                xpath_class + xpath_href + xpath_text
            )

            # Явно ждем, пока ссылка не станет кликабельной
            first_result_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(locator)
            )

            # --- Скроллим элемент в центр экрана ---
            scroll_script = "arguments[0].scrollIntoView({block: 'center'});"
            driver.execute_script(scroll_script, first_result_link)

            # --- Добавляем небольшую паузу ---
            time.sleep(0.5)

            # --- Кликаем на ссылку обычным кликом Selenium ---
            first_result_link.click()

            # Ожидаем изменения URL
            WebDriverWait(driver, 15).until(
                lambda driver: driver.current_url != BASE_URL)

        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(),
                          name="search_results_timeout",
                          attachment_type=allure.attachment_type.PNG)
            logging.error("Не дождались")
            logging.error(f"HTML: {driver.page_source}")
            assert False, "Не дождались"
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(),
                          name="search_results_error",
                          attachment_type=allure.attachment_type.PNG)
            logging.exception(f"Ошибка: {e}")
            assert False, f"Ошибка: {e}"

    with allure.step("# 4. Проверяем стр. товара"):
        try:
            # Добавим более точные проверки
            title_locator = (By.CLASS_NAME, "product-detail-page__title")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(title_locator))
            title_text = driver.find_element(*title_locator).text.lower()

            # Проверяем не только заголовок, но и наличие других элементов
            # Например, можно проверить наличие ISBN или автора
            # author_locator = (By.CLASS_NAME, "product-detail-page__author")
            # author_text = driver.find_element(*author_locator).text.lower()
            # assert "булгаков" in author_text, "Неверный автор"  # Пример

            assert title.lower() in title_text, \
                f"Нет книги: {title}"
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(),
                          name="prod_page_timeout",
                          attachment_type=allure.attachment_type.PNG)
            logging.error("Нет стр. товара")
            assert False, "Нет стр. товара"
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(),
                          name="prod_page_error",
                          attachment_type=allure.attachment_type.PNG)
            logging.exception(f"Ошибка: {e}")
            assert False, f"Ошибка: {e}"


# Тест 5

@allure.story("тест главной страницы")
def test_main_page_simplest(driver):
    """
    Открывает главную страницу, делает скриншот и проверяет title.
    """
    try:
        driver.get("https://www.chitai-gorod.ru/")  # Замените BASE_URL

        # Делаем скриншот
        allure.attach(driver.get_screenshot_as_png(),
                      name="main_page",
                      attachment_type=allure.attachment_type.PNG)

        # Проверяем, что title не пустой
        assert driver.title != "", "Title страницы пустой!"

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(),
                      name="main_page_error",
                      attachment_type=allure.attachment_type.PNG)
        assert False, f"Ошибка: {e}"
