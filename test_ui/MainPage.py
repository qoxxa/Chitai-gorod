from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import json
from DataProvider import DataProvider


class MainPage:
    def __init__(self, driver: WebDriver) ->None:
        self.url = DataProvider().get("url")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    @allure.step("Перейти на сайт")
    def go(self):
        self.driver.get(self.url)

    @allure.step("Поиск по названию")
    def find_by_title(self, title):
        find = self.wait.until(
            EC.visibility_of_element_located((By.NAME,"search"))
        )
        find.send_keys(title)
        find.send_keys(Keys.RETURN)

        resp = self.wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, title))
        )
        return resp.text

    @allure.step("Открыть карточку товара")
    def open_product_card(self, title):
        find = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, title))
        )
        find.click()

        resp = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,".product-detail-page__title"))
        )
        return resp.text

    @allure.step("Добавить в корзину")
    def add_to_cart(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='false']"))
        )
        self.driver.execute_script("arguments[0].click();", find)
        return find.text

    @allure.step("Перейти в корзину")
    def go_cart(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Корзина']"))
        )
        find.click()

    @allure.step("Кол-во товара в корзине")
    def check_quantity_in_cart(self):
        try:
            empty_cart_element = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".catalog-stub__title"))
            )
            return "Корзина уже пуста"

        except Exception:
            pass

        try:
            quantity_element = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Корзина'] div.chg-indicator"))
            )
            quantity_text = quantity_element.text

            return quantity_text

        except Exception as e:
            return f"Не удалось определить количество товаров в корзине {str(e)}"

    @allure.step("Получить наименование товара")
    def check_product_names_in_cart(self):
        try:
            empty_cart_element = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".catalog-stub__title"))
            )
            return "Нет добавленных товаров"

        except Exception:
            pass

        try:
            title_element = self.wait.until(
                 EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-cart-title__head")))
            titles = [element.text for element in title_element]
            return f"{', '.join(titles)}"

        except Exception as e:
            return f"Не удалось определить наименование товаров в корзине {str(e)}"

    @allure.step("Добавить в избранное")
    def add_to_favorites(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='В закладки']"))
        )
        self.driver.execute_script("arguments[0].click();", find)


    @allure.step("Кол-во товара в закладках и его наименование")
    def check_items_in_favorites(self):
        resp = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='Закладки'] div.chg-indicator"))
        )

        title_element = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-card__title")))

        titles = [element.text for element in title_element]
        return f"Количество в закладках: {resp.text} Наименование товара: {', '.join(titles)}"

    @allure.step("Перейти в закладки")
    def go_favorites(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Закладки']"))
        )
        find.click()

        find2 = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".bookmarks-page__title"))
        )
        return find2.text

    @allure.step("Открыть каталог")
    def open_catalog(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Каталог')]"))
        )
        self.driver.execute_script("arguments[0].click();", find)

    @allure.step("Открыть все товары каталога")
    def open_all_products(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".head-categories-menu__subtitle"))
        )
        self.driver.execute_script("arguments[0].click();", find)

    @allure.step("Фильтр по категориям и жанрам")
    def filter_by_genre(self, category, genre):
        find = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{category}')]"))
        )
        self.driver.execute_script("arguments[0].click();", find)

        find2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{genre}')]"))
        )
        self.driver.execute_script("arguments[0].click();", find2)

        find3 = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{genre}')]"))
        )
        return find3.text

    @allure.step("Сортировка товаров")
    def sort(self, index):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".catalog-products-total"))
                        )
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".chg-app-custom-dropdown__icon"))
        )
        find.click()

        find2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='app-catalog__controls']//div[{index}]"))
        )
        find2.click()

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".catalog-products-total"))
                        )
        price_elements = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product-mini-card-price__price"))
        )[:10]  # Берем первые 10

        # Извлечем цены
        prices = [int(el.text.replace("₽", "").replace(" ", "")) for el in price_elements]
        return prices

    @allure.step("Перейти в акции")
    def check_promotion(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Акции"))
        )
        self.driver.execute_script("arguments[0].click();", find)

        find2 = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".constructor-promotions-page__title"))
        )
        return find2.text

    @allure.step("Перейти в распродажу")
    def check_sales(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Распродажа"))
        )
        self.driver.execute_script("arguments[0].click();", find)

        find2 = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sales-page__title"))
        )
        return find2.text

    @allure.step("Перейти на главную, кликнув по лого сайта")
    def header_logo(self):
        find = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/']"))
        )
        self.driver.execute_script("arguments[0].click();", find)

    @allure.step("Ожидание смены URL")
    def wait_for_url_contains(self, text):
        self.wait.until(EC.url_contains(text))

    @allure.step("Добавить cookie")
    def add_cookies(self, cookie_file='cookies.json'):
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    # Убираем проблемные поля
                    cookie.pop('sameSite', None)
                    cookie.pop('expiry', None)
                    self.driver.add_cookie(cookie)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {cookie_file} не найден. Убедитесь, что он сохранён.")
        except Exception as e:
            raise Exception(f"Ошибка при добавлении cookie: {e}")

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()

    @allure.step("Проверка авторизации пользователя")
    def is_logged_in(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Константин')]"))
            )
            return True
        except:
            return False

    @allure.step("Блок с отзывами отображается")
    def book_review(self):
        find = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#reviews"))
        )
        return find

    @allure.step("Возвращение списка карточек отзывов")
    def get_review_items(self):
        items = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".review-item"))
        )
        return items

    @allure.step("Очистить корзину")
    def clear_cart(self):
        find = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-page__delete-many"))
        )
        self.driver.execute_script("arguments[0].click();", find)

        find2 = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-multiple-delete__title"))
        )
        return find2.text

    @allure.step("Очистить закладки")
    def clear_favorites(self):
        find = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bookmarks-page__delete")))
        self.driver.execute_script("arguments[0].click();", find)

        find2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Да')]")))
        find2.click()

        find3 = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[@class='catalog-stub__title']"))
        )
        return find3.text

    @allure.step("Вернуть кол-во товаров")
    def products_quantity(self):
        find = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".catalog-products-total"))
        )
        return find.text

    @allure.step("Проверка профиля")
    def check_profile(self):
        go_the_profile = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".header-controls__text"))
        )
        self.driver.execute_script("arguments[0].click();", go_the_profile)

        profile_name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".profile-page__user-name"))
                        )
        return profile_name.text

    def save_bearer_token_to_json(self, token, filename="bearer_token.json"):
        """
        Сохраняет Bearer токен в JSON файл.
        """
        if not token:
            print("Невозможно сохранить токен: токен пустой или None")
            return False

        try:
            token_data = {
                "Authorization": token,
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=4)
            print(f"Токен успешно сохранен в JSON файл: {filename}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении токена в JSON файл: {e}")
            return False


    @allure.step("Получить Bearer Token из браузера")
    def get_bearer_token(self):
        try:
            # Пример: попробуем получить из localStorage по ключу 'accessToken'
            cookies = self.driver.get_cookies()
            target_cookie_name = 'access-token'

            # Если токен найден и выглядит как Bearer (часто JWT), вернем его

            for cookie in cookies:
                if cookie['name'] == target_cookie_name:
                    token_value = cookie['value']
                    print(f"Найден токен в cookie '{target_cookie_name}': {token_value[:30]}...")  # Печатаем первые 30 символов
                    return token_value  # Возвращаем значение cookie

            # Если цикл завершился и cookie не найден
            print(f"Cookie с именем '{target_cookie_name}' не найдена.")
            return None

        except Exception as e:
            print(f"Ошибка при попытке получить токен из cookies: {e}")