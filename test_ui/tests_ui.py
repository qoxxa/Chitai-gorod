import allure
from selenium.webdriver.common.by import By
from conftest import browser, test_data


@allure.title("Авторизация по cookie")
@allure.description("Авторизация через cookie файл")
@allure.id(1)
@allure.severity("Trivial")
def test_authorization_for_cookie(ui, cookies_path):
    ui.add_cookies(cookies_path)
    ui.refresh()

    if ui.is_logged_in():
        print("✅ Успешно авторизованы!")
    else:
        print("❌ Авторизация не удалась")

    resp = ui.check_profile()
    assert resp == "Погодин Константин"
    assert "profile" in ui.driver.current_url

@allure.title("Поиск книги по названию")
@allure.description("Поиск")
@allure.id(2)
@allure.severity("Critical")
def test_search_by_title(test_data: dict, ui, title):
    search_result = ui.find_by_title(title)
    print(f'Результат поиска: {search_result}')
    assert "Идиот" in search_result, f"Текст 'Идиот' не найден в: {search_result}"
    assert "phrase=" in ui.driver.current_url

@allure.title("Открыть карточку товара")
@allure.description("Переход на страницу книги")
@allure.id(3)
@allure.severity("Critical")
def test_open_product_card(test_data: dict, ui, title):
    ui.find_by_title(title)

    product_title = ui.open_product_card(title)
    print(f"Открыта карточка товара:{product_title}")
    assert title in product_title

@allure.title("Добавить в корзину")
@allure.description("Корзина")
@allure.id(4)
@allure.severity("Blocker")
def test_add_to_cart(test_data: dict, ui, title, cookies_path):
    ui.add_cookies(cookies_path)
    ui.refresh()
    ui.find_by_title(title)
    ui.open_product_card(title)
    ui.add_to_cart()
    ui.go_cart()

    result_quantity = ui.check_quantity_in_cart()
    result_items = ui.check_product_names_in_cart()
    print (f"Количество товаров: {result_quantity}, Наименование товаров: {result_items}")
    assert title in result_items
    assert "1" in result_quantity
    assert "cart" in ui.driver.current_url

@allure.title("Очистить корзину")
@allure.description("Корзина")
@allure.id(5)
@allure.severity("Major")
def test_clear_cart(ui, cookies_path):
    ui.add_cookies(cookies_path)
    ui.refresh()
    ui.go_cart()

    cart_items = ui.check_quantity_in_cart()
    cart_quantity = ui.check_product_names_in_cart()

    print(f"Товары в корзине: {cart_items}. Наименование товара: {cart_quantity}")  # Просмотр корзины

    if cart_items == "Корзина уже пуста":
        print()
        assert "cart" in ui.driver.current_url

    else:
        clear_all_cart = ui.clear_cart()
        print(f"Результат выполнения: {clear_all_cart}") # Просмотр результата
        assert clear_all_cart == "Корзина очищена"

@allure.title("Добавить в избранное")
@allure.description("Авторизоваться на сайте и добавить в избранное")
@allure.id(6)
@allure.severity("Major")
def test_add_for_favorites(ui, cookies_path):
    ui.add_cookies(cookies_path)
    ui.refresh()
    ui.add_to_favorites()
    ui.go_favorites()

    result = ui.check_items_in_favorites()
    print(result) # Отображает кол-во и наименование товаров
    assert len(result) > 0
    assert "bookmarks" in ui.driver.current_url

@allure.title("Очистить закладки")
@allure.description("Закладки")
@allure.id(7)
@allure.severity("Major")
def test_clear_favorites(ui, cookies_path):
    ui.add_cookies(cookies_path)
    ui.refresh()
    ui.go_favorites()

    clear_all_favorites = ui.clear_favorites()
    print (f"Результат очистки закладок: {clear_all_favorites}") # Просмотр после удаления
    assert clear_all_favorites == "У вас пока нет закладок"
    assert "bookmarks" in ui.driver.current_url

@allure.title("Фильтр по категориям и жанру")
@allure.description("Поиск")
@allure.id(8)
@allure.severity("Major")
def test_filter_by_genre(test_data: dict, ui):
    category = test_data.get("category")
    genre = test_data.get("genre")

    ui.open_catalog()

    filter_genre = ui.filter_by_genre(category, genre)
    print(filter_genre)
    assert genre in filter_genre, f"Ожидалось '{genre}' в заголовке страницы, получено '{filter_genre}'"
    assert "fehntezi" in ui.driver.current_url


@allure.title("Сортировка")
@allure.description("Поиск")
@allure.id(9)
@allure.severity("Major")
def test_sort(browser, test_data: dict, ui):
    desc = test_data.get("desc")
    asc = test_data.get("asc")

    ui.open_catalog()
    ui.open_all_products()
    run_desc = ui.sort(desc)

    # Проверка, что каталог содержит товары
    quantity = ui.products_quantity()
    assert len(quantity) > 0
    print(quantity)

    # Проверка: каждое следующее число >= предыдущего (по убыванию)
    is_sorted_desc = all(current >= next for current, next in zip(run_desc, run_desc[1:]))
    assert "sortPreset=priceDesc" in browser.current_url
    assert is_sorted_desc, f"Цены не отсортированы по убыванию: {run_desc}"

    run_asc = ui.sort(asc)

    # Проверка: каждое следующее число >= предыдущего (по убыванию)
    is_sorted_asc = all(current <= next for current, next in zip(run_asc, run_asc[1:]))
    assert "sortPreset=priceAsc" in browser.current_url
    assert is_sorted_asc, f"Цены не отсортированы по возрастанию: {run_asc}"
    print(browser.current_url)

@allure.title("Навигация")
@allure.description("Переходы по основным главным кнопкам (акции, распродажа, главная кнопка)")
@allure.id(10)
@allure.severity("Major")
def test_navigation(browser, test_data: dict, ui):
    url = test_data.get("url")

    resp_promotions = ui.check_promotion()
    ui.wait_for_url_contains("promotions")

    assert "promotion" in browser.current_url
    assert resp_promotions == "СКИДКИ И АКЦИИ"
    print(resp_promotions)

    resp_sales = ui.check_sales()
    ui.wait_for_url_contains("sales")
    assert "sales" in browser.current_url
    assert  resp_sales == "Распродажа"
    print(resp_sales)

    ui.header_logo()
    ui.wait_for_url_contains(url)
    assert browser.current_url == url

@allure.title("Блок отзывов")
@allure.description("Отображение блока с отзывами и проверка списка")
@allure.id(11)
@allure.severity("Major")
def test_book_reviews(ui, title):
    ui.find_by_title(title)
    ui.open_product_card(title)
    review = ui.book_review()
    reviews = ui.get_review_items()

    assert review.is_displayed() # Блок отзывы отображается
    assert len(reviews) > 0  # Проверяем количество отзывов
    assert reviews[0].is_displayed()  # Первый отзыв виден
    print(reviews[0].text)

@allure.title("Ошибка 404")
@allure.description("Негативный тест")
@allure.id(12)
@allure.severity("Major")
def test_404_page(browser, test_data: dict, ui):
    url = test_data.get('url')
    browser.get("https://www.chitai-gorod.ru/404-test")

    assert "Страница не найдена" in browser.page_source # Код 404 (визуально)

    error_text = browser.find_element(By.CSS_SELECTOR, ".error-content").text # Текст ошибки

    assert 'Увы, но эта страница затерялась в просторах Интернета\n'
    'Но вы можете найти целые книги других страниц!\n'
    'ВЕРНУТЬСЯ НА ГЛАВНУЮ' in error_text

    ui.header_logo() # Кнопка "На главную"

    assert browser.current_url == url


@allure.title("Авторизация по cookie и получение Bearer Token")
@allure.description("Авторизация через cookie файл, получение Bearer Token и сохранение его в файл")
@allure.id(1)
@allure.severity("Critical") # Повысил важность, так как это ключевой процесс
def test_authorization_and_token(ui, cookies_path): # Объединил в один тест
    # Шаг 1: Авторизация по cookie
    ui.add_cookies(cookies_path)
    ui.refresh()

    is_logged_in = ui.is_logged_in()
    if is_logged_in:
        print("✅ Успешно авторизованы!")
    else:
        print("❌ Авторизация не удалась")

    # Шаг 2: Забрать данные Bearer Token
    bearer_token = ui.get_bearer_token()
    assert bearer_token is not None, "Bearer Token не был получен"

    # Сохраняем в JSON файл
    save_result_json = ui.save_bearer_token_to_json(bearer_token, "bearer_token.json")
    assert save_result_json, "Не удалось сохранить токен в JSON файл"

    print("✅ Bearer Token успешно получен и сохранен.")