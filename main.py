import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

from constants import EMAIL_PATTERNS, PHONE_PATTERNS, LIMITATION_URL


def search_by_pattern(patterns, text, save_list):
    """
    Ищет контакты в тексте по заданным паттернам и сохраняет в список.

    Args:
        patterns (tuple): Кортеж с регулярными выражениями для поиска.
        text (str): Текст для анализа.
        save_list (list): Список для сохранения найденных контактов.
    """

    for pattern in patterns:
        found_contacts = re.findall(pattern, text)
        if found_contacts:
            for contact in found_contacts:
                if contact not in save_list:
                    save_list.append(contact)


def contact_parser():
    """
    Парсит сайт, находит email и телефоны на всех страницах.

    Функция запрашивает URL сайта у пользователя, обходит его страницы
    (в количестве, ограниченном LIMITATION_URL) и возвращает все найденные
    email адреса и телефонные номера.
    """

    start_url = input('Введите URL сайта: ')
    urls = [start_url,]
    visited_urls = []
    phone_list = []
    email_list = []

    while urls and len(visited_urls) <= LIMITATION_URL:
        url = urls.pop()
        if url in visited_urls:
            continue

        try:
            response = requests.get(url, timeout=30)

        except requests.exceptions.RequestException:
            visited_urls.append(url)
            continue

        if response.status_code != 200:
            visited_urls.append(url)
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        visited_urls.append(url)

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('mailto:'):
                email = href[7:]
                email = email.split('?')[0]
                if email and email not in email_list:
                    email_list.append(email)
                continue

            if href.startswith('tel:'):
                phone = href[4:]
                if phone and phone not in phone_list:
                    phone_list.append(phone)
                continue

            if not href or href.startswith(('#', 'javascript:')):
                continue

            full_url = urljoin(url, href)

            if (full_url not in visited_urls and
                    full_url not in urls and
                    start_url in full_url):

                urls.append(full_url)

        text = soup.get_text()

        search_by_pattern(PHONE_PATTERNS, text, phone_list)

        search_by_pattern(EMAIL_PATTERNS, text, email_list)

    info = {'url': start_url, 'emails': email_list, 'phones': phone_list}
    return info


if __name__ == '__main__':
    print(contact_parser())
