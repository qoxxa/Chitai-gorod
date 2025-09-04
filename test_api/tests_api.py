import allure

@allure.title("Поиск фильма по id")
@allure.description("Поиск")
@allure.id(1)
@allure.severity("Critical")
def test_find_by_id(api, test_data: dict):
    id_product = test_data.get("id")
    find = api.find_by_id(id_product)

    # 🔍 Отладка
    print("Status code:", find.status_code)
    print("Request URL:", find.url)

    assert find.status_code == 200, f"Ошибка доступа: {find.status_code}" #Проверяем статус

    json_data = find.json() #Парсим JSON

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data) > 0
    with allure.step("Проверка, что id соответствует запросу"):
        assert json_data['included'][0]['id'] == id_product
    with allure.step("Проверка, что название, соответствует запросу"):
        json_data['included'][0]['attributes']['title'] == 'Идиот'
    with allure.step("Проверка, что год выхода, соответствует запросу"):
        json_data['included'][0]['attributes']['yearPublishing'] == 2025


@allure.title("Поиск фильма по заголовку")
@allure.description("Поиск")
@allure.id(2)
@allure.severity("Critical")
def test_find_by_title(api, test_data: dict):
    title = test_data.get("title")
    find = api.find_by_title(title)

    # 🔍 Отладка
    print("Status code:", find.status_code)
    print("Request URL:", find.url)

    assert find.status_code == 200, f"Ошибка доступа: {find.status_code}" #Проверяем статус

    json_data = find.json() #Парсим JSON

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data['included']) > 0, "Список included пуст"

    with allure.step("Проверка, что название соответствует запросу"):
        assert json_data['included'][0]['attributes']['title'] == 'Идиот', \
            f"Ожидалось 'Идиот', но получено {json_data['included'][0]['attributes']['title']}"

    with allure.step("Проверка, что год выпуска соответствует запросу"):
        assert json_data['included'][0]['attributes']['yearPublishing'] == 2025, \
            f"Ожидался год 2025, но получен {json_data['included'][0]['attributes']['yearPublishing']}"


@allure.title("Получить список популярных книг")
@allure.description("Поиск")
@allure.id(3)
@allure.severity("Critical")
def test_find_popular_books(api, test_data: dict):
    filter = test_data.get("filter_book")
    find = api.find_popular_books(filter)

    # 🔍 Отладка
    print("Status code:", find.status_code)
    print("Request URL:", find.url)

    assert find.status_code == 200, f"Ошибка доступа: {find.status_code}"  #Проверяем статус

    json_data = find.json() #Парсим JSON

    print(json_data)

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data) > 0

    with allure.step("Проверка, первая книга"):
        assert json_data['data'][0]['attributes']['authors'][0]['lastName'] == "Кавамура", \
            f"Ожидался автор Кавамура, но оказался {json_data['data'][0]['attributes']['authors'][0]['lastName']}"


@allure.title("Поиск автора")
@allure.description("Поиск")
@allure.id(4)
@allure.severity("Critical")
def test_find_author(api, test_data: dict):
    author = test_data.get("author")
    find = api.find_author(author)

    print("Response body:", find.text)
    print("Request URL:", find.url)
    print("Status code:", find.status_code)
    print("Response headers:", find.headers)

    assert find.status_code == 200, f"Ошибка доступа: {find.status_code}" #Проверяем статус

    json_data = find.json() #Парсим JSON

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data) > 0

    with allure.step("Проверка названия автора"):
        assert json_data['data'][0]['attributes']['title'] == "Федор Михайлович Достоевский"

    print(json_data)


@allure.title("Добавление товара в корзину")
@allure.description("Поиск")
@allure.id(5)
@allure.severity("Critical")
def test_add_to_cart(api,test_data: dict):
    json_id = test_data.get("json_id")
    add = api.add_to_cart(json_id)

    print("Response body:", add.text)
    print("Request URL:", add.url)
    print("Status code:", add.status_code)
    print("Response headers:", add.headers)

    assert add.status_code == 200, f"Ошибка доступа: {add.status_code}"  # Проверяем статус


@allure.title("Подробный просмотр корзины")
@allure.description("Поиск")
@allure.id(6)
@allure.severity("Critical")
def test_viewing_cart(api):
    view = api.viewing_cart()

    print("Response body:", view.text)
    print("Request URL:", view.url)
    print("Status code:", view.status_code)
    print("Response headers:", view.headers)

    assert view.status_code == 200, f"Ошибка доступа: {view.status_code}"  # Проверяем статус

    json_data = view.json()  # Парсим JSON

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data) > 0


@allure.title("Просмотр id товаров и общее кол-во корзины")
@allure.description("Поиск")
@allure.id(7)
@allure.severity("Critical")
def test_viewing_cart(api):
    view = api.short_viewing_cart()

    print("Response body:", view.text)
    print("Request URL:", view.url)
    print("Status code:", view.status_code)
    print("Response headers:", view.headers)

    assert view.status_code == 200, f"Ошибка доступа: {view.status_code}"  # Проверяем статус

    json_data = view.json()  # Парсим JSON

    with allure.step("Проверяем, что список не пуст"):
        assert len(json_data) > 0


@allure.title("Удаление товара из корзины")
@allure.description("Поиск")
@allure.id(8)
@allure.severity("Critical")
def test_delete_to_cart(api, test_data: dict):
    id_product = test_data.get("id_product")
    delete = api.delete_to_cart(id_product)

    print("Response body:", delete.text)
    print("Request URL:", delete.url)
    print("Status code:", delete.status_code)
    print("Response headers:", delete.headers)

    assert delete.status_code == 204, f"Ошибка доступа: {delete.status_code}"  # Проверяем статус


@allure.title("Очистка корзины")
@allure.description("Поиск")
@allure.id(9)
@allure.severity("Critical")
def test_clearing_cart(api):
    delete = api.clearing_cart()

    print("Response body:", delete.text)
    print("Request URL:", delete.url)
    print("Status code:", delete.status_code)
    print("Response headers:", delete.headers)

    assert delete.status_code == 204, f"Ошибка доступа: {delete.status_code}"  # Проверяем статус


@allure.title("Очистка корзины")
@allure.description("Поиск")
@allure.id(10)
@allure.severity("Critical")
def test_restore_product(api, test_data: dict):
    productId = test_data.get("productId")
    restore = api.restore_product(productId)


    print("Request URL:", restore.url)
    print("Status code:", restore.status_code)
    print("Response headers:", restore.headers)

    assert restore.status_code == 200, f"Ошибка доступа: {restore.status_code}"  # Проверяем статус