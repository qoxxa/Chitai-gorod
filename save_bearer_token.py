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