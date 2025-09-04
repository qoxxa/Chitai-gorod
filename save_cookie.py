from selenium import webdriver
import json
import time

# 1. Запускаем браузер
driver = webdriver.Chrome()
driver.get("https://www.chitai-gorod.ru")  # или другой сайт

# 2. Ждём, пока вы вручную войдёте в аккаунт
print("❗ Открой сайт и войди в аккаунт вручную...")
time.sleep(60)  # Даёт 60 секунд на вход

# 3. После входа — сохраняем cookie
cookies = driver.get_cookies()
with open('cookies.json', 'w') as f:
    json.dump(cookies, f, indent=2)

print("✅ Cookie сохранены в файл cookies.json")

# 4. Закрываем браузер
driver.quit()