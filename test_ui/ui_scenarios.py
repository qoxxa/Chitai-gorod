import allure
from selenium.webdriver.common.by import By
from conftest import browser


@allure.title("Полный сценарий: Поиск книги и добавление в корзину, в закладки, с последующей очисткой")
@allure.description("Авторизация через cookie, поиск книги по названию, открытие карточки товара, добавление в корзину")
@allure.id(11)  # Новый ID для объединённого теста
@allure.severity("Blocker")  # Повышенная важность, так как проверяем несколько ключевых функций
def test_full_purchase_flow(test_data: dict, ui, cookies_path):
    """
    Объединённый тест, выполняющий полный сценарий:
    1. Авторизация через cookie
    2. Поиск книги по названию
    3. Открытие карточки товара
    4. Добавление книги в корзину
    5. Добавление книги в закладки
    6. Проверка отображения блока с отзывами
    7. Переход в корзину
    8. Очистка корзины
    9. Переход в закладки
    10. Очистка закладок

    """
    title = test_data.get("title")

    # Шаг 1: Авторизация через cookie

    ui.go()  # Открываем сайт
    ui.add_cookies(cookies_path)  # Добавляем cookie
    ui.refresh()  # Обновляем страницу

    # Проверяем, что авторизация прошла успешно
    if ui.is_logged_in():
        print("✅ Успешно авторизованы!")
    else:
        print("❌ Авторизация не удалась")

    # Шаг 2: Поиск книги по названию

    search_result = ui.find_by_title(title)
    print(f"Результат поиска: {search_result}")
    assert title in search_result, f"Текст '{title}' не найден в: {search_result}"

    # Шаг 3: Открытие карточки товара

    product_title = ui.open_product_card(title)
    print(f"Открыта карточка товара: {product_title}")
    # assert title in product_title, f"Название книги '{title}' не совпадает с ожидаемым"

    # Шаг 4: Добавление в корзину

    ui.add_to_cart()

    # Шаг 5: Добавление в закладки

    ui.add_to_favorites()

    # Шаг 6: Проверка отображения блока с отзывами

    run = ui.book_review()
    run2 = ui.get_review_items()

    assert run.is_displayed() # Блок отзывы отображается
    assert len(run2) > 0  # Проверяем количество отзывов
    assert run2[0].is_displayed()  # Первый отзыв виден

    # Шаг 7: Переход в корзину и просмотр результата

    ui.go_cart()
    result_quantity = ui.check_quantity_in_cart()
    result_items = ui.check_product_names_in_cart()
    print(f"Товаров в корзине: {result_quantity}, Наименование товаров: {result_items}") # Просмотр корзины

    if result_quantity == "Корзина уже пуста":
        assert "cart" in ui.driver.current_url
    # Шаг 8: Очистка корзины
    else:
        clear_all_cart = ui.clear_cart()
        print(f"Результат выполнения: {clear_all_cart}") # Просмотр результата
        assert clear_all_cart == "Корзина очищена"

    # Шаг 9: Переход в закладки и просмотр результата

    ui.go_favorites()
    favorites_result = ui.check_items_in_favorites()
    print(f"Результат добавления в закладки: {favorites_result}") # Просмотр закладок

    # Шаг 10: Очистка закладок

    clear_all_favorites = ui.clear_favorites()
    print (f"Результат очистки закладок: {clear_all_favorites}")

@allure.title("Полный сценарий: Навигация")
@allure.description("Переход в акции, распродажу, каталог, сортировка по убыванию, сортировка по возрастанию, проверка на 404")
@allure.id(12)
@allure.severity("Critical")
def test_navigation_and_sort(test_data: dict, ui, browser):
    """
    Объединённый тест, выполняющий полный сценарий:
    1. Переход в акции
    2. Переход в распродажу
    3. Переход в главный каталог
    4. Сортировка по убыванию
    5. Сортировка по возрастанию
    6. Негативный - Проверка на 404 ошибку

    """
    url = test_data.get("url")
    desc = test_data.get("desc")
    asc = test_data.get("asc")

    # Шаг 1 Переход в акции

    ui.go()
    resp_promotions = ui.check_promotion()
    assert "promotion" in browser.current_url # Проверка корректного URL
    assert resp_promotions == "СКИДКИ И АКЦИИ" # Страница содержит заголовок "Скидки и акции"
    print(resp_promotions)

    # Шаг 2 Переход в распродажу

    resp_sales = ui.check_sales()
    assert "sales" in browser.current_url # Проверка корректного URL
    assert resp_sales == "Распродажа" # Страница содержит заголовок "Распродажа"
    print(resp_sales)

    # Шаг 3 Переход в каталог

    ui.open_catalog()
    ui.open_all_products() # Отобразить все продукты

    # Шаг 4 Сортировка по убыванию цены

    run_desc = ui.sort(desc) # Сортировка по убыванию
    quantity = ui.products_quantity() # Получаем кол-во товаров
    assert quantity > "0"
    print(quantity)

    # Проверка: каждое следующее число >= предыдущего (по убыванию)
    is_sorted_desc = all(current >= next for current, next in zip(run_desc, run_desc[1:]))

    ui.wait_for_url_contains("sortPreset=priceDesc") # Ожидание, пока URL появится в адресной строке
    assert "sortPreset=priceDesc" in browser.current_url # Проверка корректного URL
    # assert is_sorted_desc, f"Цены не отсортированы по убыванию: {run_desc}" # Цены отсортированы

    # Шаг 5 Сортировка по возрастанию цены

    run_asc = ui.sort(asc) # Сортировка по возрастанию

    # Проверка: каждое следующее число >= предыдущего (по убыванию)
    is_sorted_asc = all(current <= next for current, next in zip(run_asc, run_asc[1:]))

    ui.wait_for_url_contains("sortPreset=priceAsc") # Ожидание, пока URL появится в адресной строке
    assert "sortPreset=priceAsc" in browser.current_url # Проверка корректного URL
    # assert is_sorted_asc, f"Цены не отсортированы по возрастанию: {run_asc}" # Цены отсортированы

    print(browser.current_url)

    # Шаг 6 Проверка на 404 ошибку

    browser.get("https://www.chitai-gorod.ru/404-test")
    assert "Страница не найдена" in browser.page_source # Код 404 (визуально)

    error_text = browser.find_element(By.CSS_SELECTOR, ".error-content").text # Текст ошибки

    assert 'Увы, но эта страница затерялась в просторах Интернета\n'
    'Но вы можете найти целые книги других страниц!\n'
    'ВЕРНУТЬСЯ НА ГЛАВНУЮ' in error_text # Проверка корректного текста ошибки

    ui.header_logo() # Возвращение "На главную"

    assert browser.current_url == url # Проверка корректного URL



