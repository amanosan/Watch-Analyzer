import re

regex = r".*\/.+-.+-(.*).jpg"


def img_to_price(f):
    match = re.search(regex, str(f))
    price = float(match.group(1))
    return price
