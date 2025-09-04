import requests
from DataProvider import DataProvider
import allure


class ChitaiApi:
    @allure.step('Запрос test_api')
    def __init__(self) -> None:
        self.url2 = DataProvider().get("api2_url")
        self.url1 = DataProvider().get("api1_url")
        self.header = DataProvider().get("headers_for_auth")

    @allure.step('Поиск по id')
    def find_by_id(self, id):
     resp = requests.get(self.url2 + "search/product?phrase=" +str(id),
                         headers=self.header)
     return resp

    @allure.step('Поиск по названию')
    def find_by_title(self, title):
        resp = requests.get(self.url2 + "search/product?phrase=" + str(title),
                            headers=self.header)
        return resp

    @allure.step('Получить список популярных книг')
    def find_popular_books(self, filter):
        resp = requests.get(self.url2 + "products",
                            headers=self.header,
                            params=filter)

        return resp

    @allure.step('Поиск автора')
    def find_author(self, author):
        resp = requests.get(self.url2 + "products/facet/suggest",
                            headers=self.header,
                            params=author)

        return resp

    @allure.step('Добавление в корзину')
    def add_to_cart(self, json_id):
        resp = requests.post(self.url1 + "cart/product",
                             json=json_id,
                             headers=self.header)

        return resp

    @allure.step('Подробный просмотр корзины')
    def viewing_cart(self):
        resp = requests.get(self.url1 + "cart",
                             headers=self.header)

        return resp

    @allure.step('Просмотр id товаров и общее кол-во корзины')
    def short_viewing_cart(self):
        resp = requests.get(self.url1 + "cart/short",
                             headers=self.header)

        return resp

    @allure.step('Удаление товара из корзины')
    def delete_to_cart(self, id_product):
        resp = requests.delete(self.url1 + "cart/product/" + str(id_product),
                            headers=self.header)

        return resp

    @allure.step('Очистка корзины')
    def clearing_cart(self):
        resp = requests.delete(self.url1 + "cart",
                               headers=self.header)

        return resp

    @allure.step('Восстановление удалённого товара')
    def restore_product(self, productId):
        resp = requests.post(self.url1 + "cart/product-restore",
                               headers=self.header, json = productId)
        return resp