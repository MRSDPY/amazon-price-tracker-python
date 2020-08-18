import selenium
from selenium import webdriver
import bs4 as bs
import time


driver = webdriver.Firefox(executable_path='G:/software/geckodriver/geckodriver.exe')

driver.get("https://www.amazon.in")

# time.sleep(10)

search_b = driver.find_element_by_id("twotabsearchtextbox")

search_b.send_keys("samsung a50")

btn = driver.find_element_by_class_name("nav-input")
btn.click()

page = bs.BeautifulSoup(driver.page_source, 'html.parser')

page_link = page.find_all("a", class_="a-link-normal a-text-normal")

loop_data = {}

for i in range(len(page_link)):
    loop_data[i] = {
        "url": "https://www.amazon.in" + page_link[i]["href"],
        "name": page_link[i].span.text
    }

print("-"*50)

for i in range(len(loop_data)):
    driver.get(loop_data[i]["url"])
    saller = driver.find_element_by_id("bylineInfo").text
    
    product_name = driver.find_element_by_id("productTitle").text

    is_available = driver.find_element_by_id("availability").text

    try:
        cancle_price = driver.find_element_by_id("a-text-strike").text
    except Exception as e:
        try:
            cancle_price = driver.find_element_by_class_name("priceBlockStrikePriceString a-text-strike").tetx
        except Exception as e:
            cancle_price = "No any M.R.P is here...."

    try:
        current_price = driver.find_element_by_id("priceblock_ourprice").text
    except Exception as e:
        try:
            current_price = driver.find_element_by_id("priceblock_dealprice").text
        except Exception as e:
            try:
                current_price = driver.find_element_by_class_name("a-color-price").text
            except Exception as e:
                current_price = "Prize is not specified"

    try:
        save_money = driver.find_element_by_id("regularprice_savings").text
        save_money = save_money[9:].strip()
    except Exception as e:
        try:
            save_money = driver.find_element_by_class_name("a-span12 a-color-price a-size-base priceBlockSavingsString").text
        except Exception as e:
            save_money = "No any offer is available on this product"

    Reviews = driver.find_element_by_id("averageCustomerReviews").text

    print(f"{saller} \n {product_name}\n {cancle_price} \n {current_price} \n {save_money} \n {Reviews} \n {is_available}")
    print("*"*20)


driver.close()
