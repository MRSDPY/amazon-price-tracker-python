import bs4 as bs
import requests
import json
import re
from random_ua.random_ua import UserAgent
from random_proxy.random_proxy import Proxy
import random


def string_cleaner(sd):
    sd = sd.replace("\xa0", "")
    sd = sd.replace("\n", "")
    return sd.strip()


def build_delivery_str(sd):
    if sd is not None:
        string = sd.replace("Details", "")
        li = string.split("\n")
        li = list(filter(None, li))

        final_string = ""

        for i in li:
            final_string += " " + i.strip() + " "

        return final_string


def scrape(p_name):
    final_whole_data = {}

    ua = UserAgent()
    bot = ua.get(random.choice(["bot", "desktop"]))

    count = 0
    products = {}

    headers = {
        'User-Agent': bot,
    }

    search_topic = p_name
    search_topic = search_topic.replace(" ", "+")

    proxy = Proxy()
    main_page = proxy.get_session("post", f"https://www.amazon.in/s?k={search_topic}", headers_=headers)

    page = bs.BeautifulSoup(main_page.content, 'html.parser')
    print(page)

    page_link = page.find_all("a", class_="a-link-normal a-text-normal")

    p = re.compile(r"[\w]+:/+/+[www]*.amazon.in/+gp/+video/+")

    loop_data = {}

    for i in range(len(page_link)):
        loop_data[i] = {
            "url": "https://www.amazon.in" + page_link[i]["href"],
            "name": page_link[i].span.text
        }

    print("[-] Scrap All Data")
    for i in range(len(loop_data)):
        match = p.match(loop_data[i]["url"])
        if match is None:
            bot = ua.get(random.choice(["bot", "desktop"]))
            headers = {
                'User-Agent': bot,
            }

            inner_page = proxy.get_session("post", loop_data[i]["url"], headers_=headers)

            in_page = bs.BeautifulSoup(inner_page.content, 'html.parser')
            # saller = in_page.find_all(id="bylineInfo")[0].text

            current_price = in_page.find("span", id="priceblock_ourprice")
            if current_price is None:
                current_price = in_page.find(id="priceblock_dealprice")
                if current_price is None:
                    current_price = in_page.find(class_="a-size-medium a-color-price")
                    if current_price is None:
                        current_price = None

            save_money = in_page.find(id="regularprice_savings")

            is_avilable = in_page.find_all("div", id="availability")

            saller = in_page.find("a", id="bylineInfo")

            product_title = in_page.find("span", id="productTitle")

            delivery = in_page.find("span", id="price-shipping-message")

            rattings = in_page.find("i", class_="a-icon-star")

            Delivery_time = in_page.find("div", id="ddmDeliveryMessage")

            if is_avilable is not None and is_avilable != []:
                is_avilable = is_avilable[0].find("span")

            products[count] = {
                "Url": loop_data[i]["url"],
                "Product Name": string_cleaner(product_title.text) if product_title is not None else "No Title.",
                "Price": string_cleaner(
                    current_price.text) if current_price is not None else "No Any Price Can Define On That Page.",
                "Savings": string_cleaner(save_money.text) if save_money is not None else "No Offers Are Available.",
                "Is Available": string_cleaner(
                    is_avilable.text) if is_avilable is not None and is_avilable != [] else "No Any Stoke Are Available.",
                "Seller": string_cleaner(saller.text) if saller is not None else "Seller Is Not Mention.",
                "Ratings": rattings.text if rattings is not None else "No Ratings Can Found.",
                "Delivery Date": build_delivery_str(
                    Delivery_time.text) if Delivery_time is not None else "Delivery Time Not Specified.",
                "Delivery Charge": (delivery.text).split("\n")[
                    1] if delivery is not None else "No Any Delivery Charges Specified."
            }

            count += 1

    print("[-] Making a file")

    with open('product_data.json', 'w') as fp:
        json.dump(products, fp, indent=4)

    print("[*] Done!!!")
