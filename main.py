import requests
from bs4 import BeautifulSoup

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# получаем страницу с самыми свежими постами
ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')

# извлекаем посты
posts = soup.find_all('article', class_='post')
for post in posts:
    post_id = post.parent.attrs.get('id')
    # если идентификатор не найден, это что-то странное, пропускаем
    if not post_id:
        continue

    # получаем дату публикации
    data = post.find('header', class_='post__meta')
    data_published = data.find('span', class_='post__time').text

    # извлекаем заголовок
    title = post.find('a', class_='post__title_link').text

    # извлекаем ссылку на пост
    link = post.find('a', class_='post__title_link').get('href')

    # получаем страницу на статью
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    post = soup.find_all('div', class_='post__text post__text_v2')

    # извлекаем текст из статьи
    for contents in post:
        text = contents.text.lower()
        # ищем ключевое слово
        for key in KEYWORDS:
            if key in text:
                print(f'{data_published} | {title} | {link}')
                break
