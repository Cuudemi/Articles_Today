import json
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import hashlib
import requests

def get_headers() -> dict:
    ua = UserAgent()

    return {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }

def write_to_file(variable, name):
    if name == 'page_html':
        with open(str(name) + ".txt", "w", encoding='utf-8') as f:
            f.write(str(variable) + "\n")
    else:
        with open(str(name) + ".txt", "w", encoding='utf-8') as f:
            for e in variable:
                f.write(str(e) + "\n")


def get_articles_urls() -> dict:
    headers = get_headers()
    url = f'https://habr.com/ru/flows/develop/articles/'

    # получаем ответ в виде кода страницы
    page_html = requests.get(url, headers=headers)

    # создаем из него объект BeautifulSoup, чтобы с ним было удобнее работать
    parser = 'lxml'
    html_structure = BeautifulSoup(page_html.text, parser)
    theme = html_structure.find('h1', class_='tm-section-name__text').text
    print(theme)
    # собираем все ссылки
    all_hrefs_articles = html_structure.find_all('a', class_='tm-title__link')

    # write_to_file(page_html.text, 'page_html')
    # write_to_file(html_structure, 'html_structure')
    # write_to_file(all_hrefs_articles, 'all_hrefs_articles')

    articles = []
    for href in all_hrefs_articles:
        name = href.find('span').text
        url_article = f'https://habr.com{href.get("href")}'
        theme = theme
        articles.append(
            {
                'name': name,
                'theme': theme,
                'url': url_article
            }
        )

    return articles


def get_article_content(article_url: str, theme: str) -> dict:
    headers = get_headers()

    # получаем ответ в виде кода страницы
    page_html = requests.get(article_url, headers=headers)

    # создаем из него объект BeautifulSoup, чтобы с ним было удобнее работать
    parser = 'lxml'
    html_structure = BeautifulSoup(page_html.text, parser)

    article_name = html_structure.find('h1', 'tm-title tm-title_h1').find('span').text
    article_blocks_content = html_structure.find('div', 'article-formatted-body').find_all(['p', 'h2', 'img'])

    # обработка содержимого изображения
    article_text = []
    for block in article_blocks_content:
        match block.name:
            case 'img':
                img_src = block.get('src')
                img_filename = f"{get_hash_filename(img_src)}.png"
                upload_image(img_src, img_filename)

                article_text.append(f"<img src={img_filename}'/>")
            case 'p':
                article_text.append(f"<p>{block.text}</p>")
            case 'h2':
                article_text.append(f"<h>{block.text}</h>")

    article_content = {
        "id": re.search(r"https://habr.com/ru/.*articles/(.*)/", article_url).group(1),
        "name": article_name,
        'theme': theme,
        "url": article_url,
        "text": article_text,
    }

    return article_content

def upload_image(src, img_filename):
    path_image = f"Parser/output/images/{img_filename}"
    img_data = requests.get(src).content
    
    with open(path_image, 'wb') as handler:
        handler.write(img_data)

def write_file_json(article: dict):
    path = f"Parser/output/{article['id']}.json"
    with open(path, "w", encoding='utf-8') as file:
        try:
            json.dump(article, file, indent=4, ensure_ascii=False)
        except Exception as e: print(e)


def get_hash_filename(filename: str) -> str:
    return hashlib.md5(filename.encode('utf-8')).hexdigest()

if __name__ == '__main__': 
    articles_urls = get_articles_urls()
    for article in articles_urls:
        url = article['url']
        article_content = get_article_content(url, article['theme'])

        write_file_json(article_content)
        #print(article_content)