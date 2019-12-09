import requests
import csv
from bs4 import BeautifulSoup as soup
from datetime import date

today = date.today()
date = today.strftime("%m/%d/%y")

# appending data to csv
writer = open("Abercrombie_Data.csv", "a")

# grabbing the pages and parsing into html
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

links = open('Abercrombie_Links.txt', 'r')
types = links.readlines()
links.close()

for type in types:
    html = requests.get(type,headers=headers)
    page_soup = soup(html.text,"html.parser")

    # grabs each product
    containers = page_soup.findAll("div",{"class": "product-template ds-override"})

    ## first time creating csv
    # writing the csv
    # filename = "abercrombie.csv"
    # f = open(filename, "w")
    # f.write("Date,Category,Product Name,Product Color,Original price,Sale price,Promotion \n")

    # general info for all products
    promotion_container = page_soup.findAll("span",{"class":"desktop"})
    promotion = promotion_container[0].text

    category_text = page_soup.title.text.split('|')
    category = category_text[0].strip()

    # for loop for all products
    for container in containers:
        sku_container = container.findAll("button",{"class":"button ds-override overlay-button product-card__button product-card__button--l product-card__button--save"})
        sku = sku_container[0]["data-product-id"]

        product_container = container.findAll("a",{"class":"product-card__name"})
        product_name = product_container[0].text

        if ("Icon" in product_name or "Logo" in product_name):
            continue

        color_container = container.findAll("a",{"class":"product-card__image-link"})
        product_color = color_container[0].img["alt"].split(',')
        color = product_color[1].title()

        price_container = container.findAll("span",{"class":"product-price-text ds-override"})
        if(len(price_container)>1):
            sale_price = price_container[1].text
            original_price = price_container[0].text
        else:
            original_price = price_container[0].text
            sale_price = ""

        extra_promo_container = container.findAll("span",{"class":"promo-badge"})
        if(len(extra_promo_container)>0):
            extra_promo = extra_promo_container[0].text
        else:
            extra_promo = ""

        writer.write(date + "," + category + "," + product_name.strip() + "," + color.strip() + "," + sku.strip() + "," + original_price.strip() + "," + sale_price.strip() + "," + promotion.strip() +  "," + extra_promo.strip() + "\n")

writer.close()
