# Проект: Автоматизированные тесты для сайта Читай-город

# Задача

Данный проект предназначен для автоматизации тестирования веб-сайта chitai-gorod.ru. Тесты охватывают как и функциональность пользовательского интерфейса (UI), так и API. Основная цель проекта - обеспечить качество и стабильность приложения через выполнение автоматизированных тестов.

## Запуск тестов

Для запуска тестов выполните следующие шаги:
1. Склонировать проект

2. Убедитесь, что у вас установлены все зависимости, указанные в файле `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите тесты с генерацией отчётности, используя один из следующих режимов:
   - Запуск UI - тестов:
      ```bash
     pytest -s -v --alluredir=allure-result test_ui.py
     ```
     
   - Запуск UI тестовых сценариев:
      ```bash
     pytest -s -v --alluredir=allure-result test_ui/ui_scenarios
     ```
     
   - Запуск API - тестов: 
   ```bash
   pytest -s -v --alluredir=allure-result test_api
   ```
   и откройте отчёт с помощью команды:
   ```bash
        allure serve allure_result
   ```
   
4. Для автоматизации отчётности allure, используйте скрипт `run.sh` командой
   ```bash
   ./run.sh
   ```



3.Запустите тесты с генерацией отчётности, используя один из следующих режимов:
    - Запуск UI-тестов:
        ```bash
        pytest -s -v --alluredir=allure-results test_ui/tests_ui.py
        ```

## Структура проекта

Chitai-gorod/
│
├── 📄 requirements.txt # Зависимости Python
├── 📄 pytest.ini # Конфигурация pytest
├── 📄 run.sh # Скрипт запуска тестов и генерации отчета
├── 📄 test_data.json # Файл с тестовыми данными
├── 📄 save_bearer_token.py # Скрипт для получения и сохранения Bearer токена
├── 📄 save_cookie.py # Скрипт для сохранения cookie после ручной авторизации
├── 📄 .gitignore # Список файлов, исключённых из Git
│
├── 📄 DataProvider.py # Утилита для получения данных из test_data.json
├── 📄 conftest.py # Глобальные фикстуры и настройки Pytest
│
├── 📂 test_api/ # API-тесты
│ ├── 📄 BoardApi.py # Методы для работы с API
│ └── 📄 tests_api.py # Тестовые сценарии API
│
└── 📂 test_ui/ # UI-тесты
├── 📄 MainPage.py # Page Object Модели для UI
├── 📄 tests_ui.py # Тестовые сценарии UI
└── 📄 ui_scenarios.py # Сценарии пользовательских путей