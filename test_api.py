from typing import Generator
import requests
import pytest
import allure
from conftest import (
    HEADERS,
    BASE_URL,
    BOOK1_ID_IN_CATALOG,
    BOOK2_ID_IN_CATALOG,
    BOOK_NAME,
    BODY_AD_DATA
)


@pytest.fixture
def get_book_id_from_cart(add_book_to_cart: Generator) -> int:
    URL = f'{BASE_URL}/api/v1/cart'
    # получение карзины
    response = requests.request("GET", URL, headers=HEADERS)
    book_id = response.json()["products"][0]['id']
    return book_id


@pytest.fixture
def clear_cart() -> Generator:
    URL = f'{BASE_URL}/api/v1/cart'
    requests.request("DELETE", URL, headers=HEADERS)
    yield
    requests.request("DELETE", URL, headers=HEADERS)


@pytest.fixture
def delete_book_from_cart(get_book_id_from_cart) -> Generator:
    # действия до вызова тестовой функции
    book_id = get_book_id_from_cart
    URL = f'{BASE_URL}/api/v1/cart/product/{book_id}'

    yield

    # действия после вызова тестовой функции
    requests.request("DELETE", URL, headers=HEADERS)


@pytest.fixture
def add_book_to_cart() -> Generator:
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    yield


@allure.story("Проверка добавления книги в корзину")
def test_add_book(delete_book_from_cart: Generator) -> None:
    """
    Функция добавляет книгу в корзину,
    и проверяет что запрос выполнен
    """
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    response = requests.post(URL, headers=HEADERS, json=body)
    assert response.status_code == 200


@allure.story("Проверка получение пустой корзины")
def test_get_cart() -> None:
    """
    Функция получает корзину,
    проверет что запрос выполнен и корзина пустая
    """
    URL = f'{BASE_URL}/api/v1/cart'
    # получение карзины
    response = requests.request("GET", URL, headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["products"] == []


@allure.story("Проверка получения товара по ключевому слову")
def test_get_by_keyword() -> None:
    """
    Функция вводит ключевое слово в поисковую строку и
    проверяет, что запрос выполнен
    """
    URL = (
      f'{BASE_URL}'
      '/api/v2/search/product?customerCityId=213&products'
      f'[page]=1&products[per-page]=60&phrase={BOOK_NAME}&abTestGroup=1'
    )
    body = {
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    response = requests.get(URL, headers=HEADERS, json=body)
    assert response.status_code == 200


@allure.story("Проверка удаления книги из корзины")
def test_delete_book_from_cart(
    get_book_id_from_cart: int,
    add_book_to_cart: Generator
) -> None:
    """
    Функция удаляет книгу из корзины и
    проверяет, что запрос выполнен
    """
    book_id = get_book_id_from_cart
    URL = f'{BASE_URL}/api/v1/cart/product/{book_id}'
    response = requests.request("DELETE", URL, headers=HEADERS)
    assert response.status_code == 204


@allure.story("Проверка общей стоимости корзины")
def test_total_cost(clear_cart: Generator) -> None:
    """
    Функция добавляет две книги в корзину, складывает сумму
    стоимости книг и сверяет с итоговой суммой
    """
    # добавление двух книг
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    body = {
        "id": BOOK2_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    # получение корзины
    URL = f'{BASE_URL}/api/v1/cart'
    response = requests.request("GET", URL, headers=HEADERS)

    total_cost = response.json()["costWithSale"]
    cost1 = response.json()["products"][0]["cost"]
    cost2 = response.json()["products"][1]["cost"]

    assert cost1 + cost2 == total_cost
