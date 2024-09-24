from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


def get_wikipedia_article(browser, search_query):
    """Функция для открытия страницы на Википедии по запросу."""
    url = f"https://ru.wikipedia.org/wiki/{search_query.replace(' ', '_')}"
    browser.get(url)
    time.sleep(2)  # Подождем пока страница загрузится
    if "Wikipedia" in browser.title or "Википедия" in browser.title:
        return True
    else:
        print("Статья не найдена.")
        return False


def print_paragraphs(browser):
    """Функция для листания параграфов статьи."""
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for idx, paragraph in enumerate(paragraphs, 1):
        print(f"\nПараграф {idx}: {paragraph.text.strip()}")
        if idx % 5 == 0:  # Листаем по 5 параграфов
            if input("Продолжить просмотр? (Да/Нет): ").lower() != 'да':
                break


def get_internal_links(browser):
    """Функция для получения внутренних ссылок на связанные статьи."""
    links = browser.find_elements(By.TAG_NAME, "a")
    internal_links = [link for link in links if link.get_attribute('href') and '/wiki/' in link.get_attribute('href')]
    return internal_links


def main():
    # Запуск браузера
    browser = webdriver.Firefox()

    try:
        browser.get(
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        first_request = input("Введите первоначальный запрос: ")

        if get_wikipedia_article(browser, first_request):
            while True:
                print('''\nВыберите вариант дальнейших действий:
                1. Листать параграфы текущей статьи
                2. Перейти на одну из связанных страниц
                3. Выйти из программы
                ''')
                second_request = input("Ваш выбор?: ")

                if second_request == '1':
                    # Листаем параграфы текущей статьи
                    print_paragraphs(browser)

                elif second_request == '2':
                    # Переход на случайную связанную статью
                    internal_links = get_internal_links(browser)
                    if internal_links:
                        random_link = random.choice(internal_links)
                        new_article_url = random_link.get_attribute('href')
                        print(f"Переходим на связанную страницу: {new_article_url}")
                        browser.get(new_article_url)
                        time.sleep(2)
                    else:
                        print("Связанные страницы не найдены.")

                elif second_request == '3':
                    if input("Хотите выйти? (Да/Нет): ").lower() in ['да', 'y', 'yes']:
                        print("Выход из программы.")
                        break
                else:
                    print("Неверный ввод. Пожалуйста, попробуйте снова.")

    finally:
        time.sleep(2)
        browser.quit()


if __name__ == '__main__':
    main()
