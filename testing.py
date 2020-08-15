import bs4 as bs
import requests
import re

final_whole_data = {}

count = 0
products = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
}

search_topic = input("Enter any thing that you wan't to search : ")
search_topic = search_topic.replace(" ", "+")

main_page = requests.post(f"https://www.amazon.in/s?k={search_topic}", headers=headers)

page = bs.BeautifulSoup(main_page.content, 'html.parser')

page_link = page.find_all("a", class_="a-link-normal a-text-normal")

loop_data = {}

p = re.compile(r"[\w]+:/+/+[www]*.amazon.in/+gp/+video/+")

for i in range(len(page_link)):
    loop_data[i] = {
        "url": "https://www.amazon.in" + page_link[i]["href"],
        "name": page_link[i].span.text
    }

for i in range(len(loop_data)):
    match = p.match(loop_data[i]["url"])
    if match is None:
        inner_page = requests.post(loop_data[i]["url"], headers=headers)
        in_page = bs.BeautifulSoup(inner_page.content, 'html.parser')

        rattings = in_page.find("div", id="ddmDeliveryMessage")
        product_title = in_page.find("span", id="productTitle")

        if rattings is not None:
            print("Delivery Time:", rattings.text.strip())
        if product_title is not None:
            print("Product:", product_title.text.strip())
