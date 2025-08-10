from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class LoginPage:
    """
    Page Object для страницы входа "Читай-город" (модальное окно).
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Локаторы для элементов в модальном окне
        self.phone_input = (By.ID, "tid-input")
        self.get_code_button = (By.XPATH, "//div[text()='Получить код']")

    @allure.step("Ввести номер телефона: {phone_number}")
    def enter_phone_number(self, phone_number: str):
        """
        Вводит указанный номер телефона в соответствующее поле.
        """
        phone_field = self.wait.until(
            EC.presence_of_element_located(self.phone_input)
        )
        phone_field.clear()
        phone_field.send_keys(phone_number)

    @allure.step("Получить введенный номер телефона")
    def get_phone_number(self) -> str:
        """
        Возвращает текущее значение из поля ввода номера телефона.
        """
        phone_field = self.wait.until(
            EC.presence_of_element_located(self.phone_input)
        )
        return phone_field.get_attribute("value")

    @allure.step("Проверить, активна ли кнопка 'Получить код'")
    def is_get_code_button_enabled(self) -> bool:
        """
        Проверяет, является ли кнопка 'Получить код' кликабельной.
        """
        try:
            self.wait.until(
                EC.element_to_be_clickable(self.get_code_button)
            )
            return True
        except Exception:  # Убираем переменную 'e', если она не используется
            # Можно добавить более детальное логирование, если нужно
            # print(f"Кнопка 'Получить код' не активна: {e}")
            return False

    @allure.step("Нажать кнопку 'Получить код'")
    def click_get_code_button(self):
        """
        Нажимает на кнопку 'Получить код'.
        """
        button = self.wait.until(
            EC.element_to_be_clickable(self.get_code_button)
        )
        button.click()
