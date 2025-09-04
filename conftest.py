import pytest
import allure
from selenium import webdriver
from DataProvider import DataProvider
from test_api.BoardApi import ChitaiApi
from test_ui.MainPage import MainPage


@pytest.fixture(scope='session')
def browser():
    with allure.step("Открыть и настроить браузер"):
        timeout = DataProvider().getint('timeout')
        browser_name = DataProvider().get('browser_name').lower()

        if browser_name == 'chrome':
            browser = webdriver.Chrome()
        elif browser_name == 'firefox':
            browser = webdriver.Firefox()
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}. Поддерживаются: 'chrome', 'firefox'.")

        browser.implicitly_wait(timeout)
        browser.set_window_size(1280, 1024)
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()

@pytest.fixture(scope='session')
def test_data():
    return DataProvider()

@pytest.fixture
def ui(browser):
    ui = MainPage(browser)
    ui.go()
    return ui

@pytest.fixture
def api():
    return ChitaiApi()

@pytest.fixture
def title(test_data):
    return test_data.get("title")

@pytest.fixture
def cookies_path(test_data):
    return test_data.get("cookies_path")
