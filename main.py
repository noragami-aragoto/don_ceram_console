import requests
from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint as print

DOMAIN = 'https://donceram.ru'


def app(params, url):
    if params == 'collection':
        parse_collection(url)
    elif params == 'brand':
        parse_brand(url)


def parse_collection(url):
    dom = get_dom(url)
    title = dom.xpath('//h1')[0].text
    pictures = find_urls_collection_img_card(dom)
    products_urls = find_urls_collection_product_card(dom)
    products = []
    for product_url in products_urls:
        products.append(parse_product_card(product_url))
    print(products)


def parse_product_card(url):
    dom = get_dom(url)
    title = dom.xpath('//h1')[0].text
    features = get_product_features(dom)
    pictures = get_product_images(dom)
    return {
        'title': title,
        'features': features,
        'pictures': pictures,
    }


def get_product_images(dom):
    elements = dom.xpath("//a[contains(@style,'back')] ")
    result = []
    for element in elements:
        result.append(DOMAIN + str(element.get('style')).split(':url(')[-1].replace(')', ''))
    return set(result)


def get_product_features(dom):
    elements = dom.xpath("//div[@class='product__fields-field']/*")
    flag = True
    result = {}
    for element in elements:
        if flag:
            key = element.text
            flag = False
        else:
            result[key] = element.text
            flag = True
    return result


def find_urls_collection_img_card(dom):
    result = []
    elements = dom.xpath("//img[@class='slide']")
    for element in elements:
        result.append(DOMAIN + element.get('src'))
    return set(result)


def find_urls_collection_product_card(dom):
    result = []
    elements = dom.xpath("//div[@class='collection__products-product']//a[1]")
    for element in elements:
        result.append(DOMAIN + element.get('href'))
    return result


def parse_brand():
    pass


def get_html(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def get_dom(url):
    html = get_html(url)
    bs = BeautifulSoup(html, 'html.parser')
    return etree.HTML(str(bs))


if __name__ == '__main__':
    app('collection', 'https://donceram.ru/katalog_dizayn_proektov/gravity_ibero_keraben_sovmeschennyy_sanuzel')
