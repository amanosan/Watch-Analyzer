import requests
import pandas as pd
import os

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

# uncomment below 3 lines to make required directories
# os.mkdir('./images')
# for brand in BRANDS:
#     os.mkdir(f"./images/{brand}")

for brand in BRANDS:
    df = pd.read_csv(f'./data/{brand}.txt', names=['link', 'price'])

    for i in range(len(df)):
        img_link = df.link[i]
        price = df.price[i]

        img = requests.get(img_link)
        if not img.ok:
            continue

        #  file name format - "brand-index-price.jpg"
        with open(f"./images/{brand}/{brand}-{i+1}-{price}.jpg", "wb+") as file:
            file.write(img.content)
