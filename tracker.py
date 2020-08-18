from use_bs import scrape
import json
import smtplib
import os


# product_name = input("Enter product name : ")
price_range = input("Enter price range (e.x: <20000 and >20000) : ")
price_con = price_range[0]
#
# scrape(product_name)
#
with open("product_data.json", "r") as f:
    data = f.read()

dict_data = json.loads(data)
make_string = """"""
c = 1

for i in range(len(dict_data)):
    if dict_data[str(i)]["Price"] != "No Any Price Can Define On That Page.":
        if price_con == "<":
            if int(dict_data[str(i)]["Price"].split(".")[0].replace(",", "")) < int(price_range[1:]):
                for k, v in dict_data[str(i)].items():
                    if k == "Url":
                        make_string += f"{c}) {k} : {v}\n"
                        c += 1
                    else:
                        make_string += f"     {k} : {v}\n"
        else:
            if int(dict_data[str(i)]["Price"].split(".")[0].replace(",", "")) > int(price_range[1:]):
                for k, v in dict_data[str(i)].items():
                    if k == "Url":
                        make_string += f"{c}) {k} : {v}\n"
                        c += 1
                    else:
                        make_string += f"     {k} : {v}\n"
try:
    m = smtplib.SMTP(host="smtp-relay.sendinblue.com", port=587)
    m.ehlo()
    m.starttls()
    m.login(os.environ.get("Email"), os.environ.get("Email_pass"))

    m.sendmail("mgidshubham@gmail.com", "sdankhara1@gmail.com", make_string)

    m.close()
except smtplib.SMTPException as e:
    print(e.message)
