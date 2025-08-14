import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv
import os


@pytest.fixture(scope="session")
def driver():  # Убрали -> WebDriver
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    # --- Добавляем user-agent ---
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    # ---

    driver_instance = webdriver.Chrome(options=options)
    driver_instance.maximize_window()
    driver_instance.implicitly_wait(50)
    yield driver_instance
    driver_instance.quit()


# test_api.py
load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

HEADERS = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
      'Authorization': bearer_token
    }

BOOK1_ID_IN_CATALOG = 2968841
BOOK2_ID_IN_CATALOG = 2713476
BOOK_NAME = "танах"

BASE_URL = "https://web-agr.chitai-gorod.ru/web"

BODY_AD_DATA = {"product_shelf": "", "item_list_name": "search"}
