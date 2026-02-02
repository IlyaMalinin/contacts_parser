import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_patterns = [
    r'\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',  # +7 999 123 45 67
    r'8\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}',     # 8 999 123 45 67
    r'\+7-\d{3}-\d{3}-\d{2}-\d{2}',           # +7-999-123-45-67
    r'\b\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b',  # 999-123-45-67
    r'\(\d{3}\)\s?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}',  # (999) 123-45-67
]

start_url = input('Введите URL сайта: ')
urls = [start_url,]
visited_urls = []
phone_list = []
mail_list = []

while urls:
    url = urls.pop()
    if url in visited_urls:
        continue

    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        print(f"Ошибка {response.status_code} для {url}")
        visited_urls.append(url)
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    visited_urls.append(url)
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
            continue
        full_url = urljoin(url, href)
        if (full_url not in visited_urls and 
                full_url not in urls and
                start_url in full_url):

            urls.append(full_url)

    text = soup.get_text()
    for patern in phone_patterns:
        found_phone = re.findall(patern, text)
        if found_phone:
            for phone in found_phone:
                if phone not in phone_list:
                    phone_list.append(phone)
    found_emails = re.findall(email_pattern, text)
    if found_emails:
        for email in found_emails:
            if email not in mail_list:
                mail_list.append(email)

info = {'url': start_url, 'emails': mail_list, 'phones': phone_list}

print(info)
