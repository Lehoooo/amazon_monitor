# https://cats.fish :)
import time
import requests
from bs4 import BeautifulSoup
import re
import threading


def get_amazon_product_data(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    results = []
    for product in products:
        title_element = product.find(
            'span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        price_element = product.find('span', {'class': 'a-price-whole'})
        cents_element = product.find('span', {'class': 'a-price-fraction'})
        url_element = product.find('a',
                                   {'class': 'a-link-normal s-no-outline'})
        rrp_element = product.find('span', {'class': 'a-price a-text-price'})
        if title_element and price_element:
            title = title_element.text.strip()
            price = price_element.text.strip()
            cents = cents_element.text.strip()
            b = 'https://www.amazon.com.au' + url_element['href']

            url = re.sub(r'/dp/([^/]+)/.*', r'/dp/\1', b) + "?m=a1ge4gwd4xc0d9"

            if rrp_element:
                rrp = rrp_element.find('span', {'class': 'a-offscreen'})
                if rrp:
                    rrp = rrp.text.strip()
                else:
                    rrp = 'N/A'
            else:
                rrp = 'N/A'

            print(title)
            print(price + cents)
            print(url)
            print(rrp)
            print()

            results.append({
                'title': title,
                'price': price + cents,
                'url': url,
                'rrp': rrp
            })

    return results


def monitor_amazon_products(url):
    product_data = get_amazon_product_data(url)
    print("init")

    while True:
        new_product_data = get_amazon_product_data(url)
        print("checking")

        for product in new_product_data:
            if product not in product_data:
                product_data.append(product)
                print(f"New Product:")
                print(f"Title: {product['title']}")
                print(f"Price: {product['price']}")
                print(f"RRP: {product['rrp']}")
                print(f"URL: {product['url']}")
                with open("/app/aaa.txt", "a") as f:
                    f.write(f"New Product:\n")
                    f.write(f"Title: {product['title']}\n")
                    f.write(f"Price: {product['price']}\n")
                    f.write(f"RRP: {product['rrp']}\n")
                    f.write(f"URL: {product['url']}\n")
                    f.write(
                        f"------------------------------------------------\n")

                json_data = {
                    'chat_id':
                    'chatidhere',
                    'text':
                    'Title: ' + product['title'] +
                    '\nPrice: $' + product['price'] + '\nRRP: ' +
                    product['rrp'] + '\nURL: ' + product['url'],
                }
                response = requests.post(
                    'https://api.telegram.org/apitokenshithere/sendMessage',
                    json=json_data,
                )
                print(response.status_code)

        time.sleep(30)  # Wait for 5 minutes before checking again


url = 'https://www.amazon.com.au/s?i=grocery&bbn=8415198051&dc&qid=1684717509&ref=sr_nr_i_19' # for grocery 1st page
print("hi :)")
monitor_thread = threading.Thread(target=monitor_amazon_products, args=(url, ))
monitor_thread.start()
print("aa")
