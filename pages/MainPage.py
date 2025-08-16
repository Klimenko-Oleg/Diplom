from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from config import BASE_URL


class MainPage:
    """Page Object для главной страницы "Читай-город"."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(BASE_URL)
        self.wait = WebDriverWait(driver, 15)

        # Локаторы:
        self.search_input = (By.NAME, "search")
        self.search_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.login_button = (By.XPATH, "//span[text()='Войти']")
        self.cart_icon = (
            By.XPATH,
            "//span[@class='header-controls__text' "
            "and contains(text(), 'Корзина')]")

    @allure.step("Ввести поисковый запрос: {query}")
    def search(self, query):
        # Ждем загрузки страницы
        self.wait.until(
            lambda driver: driver.execute_script(
                'return document.readyState=="complete"')
        )

        search_input = self.wait.until(
            EC.presence_of_element_located(self.search_input)
        )
        search_input.send_keys(query)
        search_button = self.wait.until(
            EC.element_to_be_clickable(self.search_button)
        )
        search_button.click()

    @allure.step("Перейти на страницу входа")
    def go_to_login_page(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_button.click()

    @allure.step("Проверить, что главная страница отображается")
    def is_main_page_displayed(self):
        try:
            self.wait.until(
                EC.presence_of_element_located(self.search_input)
            )
            return True
        except Exception as e:
            print(f"Ошибка при проверке: {e}")
            return False

    @allure.step("Открыть корзину")
    def open_cart(self):
        cart_icon = self.wait.until(
            EC.element_to_be_clickable(self.cart_icon)
        )
        cart_icon.click()

    @allure.step("Проверить основные элементы главной страницы")
    def check_main_page_elements(self):
        """Проверяет наличие основных элементов на главной странице."""
        with allure.step("Проверка наличия поля поиска"):
            self.wait.until(EC.presence_of_element_located(self.search_input))
        with allure.step("Проверка наличия кнопки поиска"):
            self.wait.until(EC.element_to_be_clickable(self.search_button))
        with allure.step("Проверка наличия кнопки входа"):
            self.wait.until(EC.element_to_be_clickable(self.login_button))
        with allure.step("Проверка наличия иконки корзины"):
            self.wait.until(EC.element_to_be_clickable(self.cart_icon))
