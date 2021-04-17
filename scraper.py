import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome('chromedriver.exe')

BRANDS = [
    'rolex',
    'audemarspiguet',
    'breitling',
    'iwc',
    'jaegerlecoultre',
    'omega',
    'panerai',
    'patekphilippe',
    'cartier',
    'gucci',
    'seiko',
    'movado',
    'zenith'
]

for brand in BRANDS:
    urls = [
        f'https://www.chrono24.com/{brand}/index.htm',
        f'https://www.chrono24.com/{brand}/index-2.htm',
        f'https://www.chrono24.com/{brand}/index-3.htm',
        f'https://www.chrono24.com/{brand}/index-4.htm',
        f'https://www.chrono24.com/{brand}/index-5.htm',
    ]

    for url in urls:
        browser.get(url)
        time.sleep(5)  # waiting for page to load
        # scrolling so that images get loaded
        for _ in range(16):
            browser.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)

        page_source = browser.page_source

        # parsing the page
        page = bs(page_source, 'html.parser')

        article_divs = page.find_all(
            'div', {'class': 'article-item-container'})

        img_links = []
        prices = []
        for article in article_divs:
            img_link = article.find(
                'div', {'class': 'article-image-container'}).div.img['src']

            price_text = article.find('strong').text
            price_text = ''.join(filter(str.isdigit, price_text))

            # checking if links/prices are empty or not present
            if not img_link or not price_text:
                continue
            if img_link == "" or price_text == "":
                continue

            # if everthing is fine, we append to the list
            img_links.append(img_link)
            prices.append(price_text)

        # writing the content into a file:
        with open(f"./data/{brand}.txt", "a+") as file:
            for (url, price) in zip(img_links, prices):
                file.write(f"{url}, {price}\n")

browser.close()
