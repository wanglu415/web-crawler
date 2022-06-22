import bs4
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup
import csv

url = 'https://www.newegg.com/p/pl?d=graphics+cards'

client = request(url)
page_html = client.read()
client.close()

page_soup = soup(page_html, 'html.parser')
cells = page_soup.find_all("div", attrs={"class": "item-cell"})

with open('graphics_cards.csv', mode='w', newline='') as graphics_cards_file:
    file_writer = csv.writer(graphics_cards_file)
    file_writer.writerow(['Brand', 'Product Name', 'Price', 'Shipping'])
    for cell in cells:
        if cell.find("div", attrs={"class": "txt-ads-link"}) == None:
            try:
                brand_tag = cell.find_all("div", attrs={"class": "item-branding"})
                brand_name = brand_tag[0].img["title"]
              
                title_tag = cell.find_all("a", attrs={"class": "item-title"})
                product_name = title_tag[0].text

                if cell.find_all("p", attrs={"class": "item-promo"}) != []:
                    price_tag = cell.find_all("p", attrs={"class": "item-promo"})
                    pricing_info = price_tag[0].text

                    if cell.find_all("a", attrs={"class": "shipped-by-newegg"}) != []:
                        shipping_tag = cell.find_all("a", attrs={"class": "shipped-by-newegg"})
                        shipping_info = shipping_tag[0].text
                    else:
                        shipping_tag = cell.find_all("li", attrs={"class": "price-ship"})
                        shipping_info = shipping_tag[0].text
                else:
                    price_tag = cell.find_all("li", attrs={"class": "price-current"})
                    dollar_sign = price_tag[0].text[0]
                    dollars = price_tag[0].strong.text
                    cents = price_tag[0].sup.text
                    pricing_info = dollar_sign + dollars + cents

                    shipping_tag = cell.find_all("li", attrs={"class": "price-ship"})
                    shipping_info = shipping_tag[0].text
            except Exception as error:
                print(f'Error that occurred: {error.__class__.__name__}')
                print(f'Error message: {error}')
                print(f'Cell where error occurred: {cell}')
            finally:
                file_writer.writerow([brand_name, product_name, pricing_info, shipping_info])
