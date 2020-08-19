from use_bs4 import scrape
import json
import smtplib
import os
from email.mime import multipart
from email.mime.text import MIMEText


def send_mail(host_name=None, port=587,smtp_id=None, smtp_pass=None, from_email="mgidshubham@gmail.com", to_email=None, subject="Amazon Price Compare Result", message=None, html_contact=None):
    assert isinstance(to_email, list)
    try:
        smtp = multipart.MIMEMultipart('alternative')
        smtp['From'] = from_email
        smtp['To'] = "-".join(to_email)
        smtp['Subject'] = subject

        ms = ""

        if message is not None:
            ms = MIMEText(make_string, "plain")

        if html_contact is not None:
            ms = MIMEText(html_contact, "html")

        smtp.attach(ms)

        m = smtplib.SMTP(host=host_name, port=port)
        m.ehlo()
        m.starttls()
        m.login(smtp_id, smtp_pass)

        m.sendmail(from_email, to_email, smtp.as_string())

        m.close()
    except smtplib.SMTPException as e:
        print(e)


product_name = input("Enter product name : ")
price_range = input("Enter price range (e.x: <20000 and >20000) : ")
price_con = price_range[0]

scrape(product_name)

with open("product_data.json", "r") as f:
    data = f.read()

dict_data = json.loads(data)
make_string = """
<!DOCTYPE html>
<html>
<title>Web Page Design</title>
<head>
<style type="text/css">
    
    body{
    text-align: center;
    color: white;
}

.sd-main{
    padding: 10px;
    font-size: 20px;
}

.sd-main i{
    text-decoration: none;
    text-decoration-style: none;
    font-weight: bold;
    color: #FFB320;
    border-bottom: 2px solid #FFB320;
}

.sd-main a{
    color: white;
    text-decoration: none;
}

.main-container{
    margin: 20px;
    background-color: rgba(0,0,0,1);
    border-radius: 30px;
    border: 4px solid #FFB320;
    padding: 16px;
}


</style>
</head>
<body>
<div class="main-container" >
"""
c = 1

for i in range(len(dict_data)):
    if dict_data[str(i)]["Price"] != "No Any Price Can Define On That Page.":
        if price_con == "<":
            try:
                if int((dict_data[str(i)]["Price"].split(".")[0].replace(",", "")).replace("₹", "")) < int(price_range[1:]):
                    for k, v in dict_data[str(i)].items():
                        if k == "Url":
                            make_string += f"<div class='sd-main' >{c})<br/><i> {k} :</i> <a href='{v}'>{v}</a><br/><br/>"
                            c += 1
                        else:
                            make_string += f"<i>{k} : </i>{v}<br/><br/>"
                    make_string += "</div>"
            except ValueError as e:
                print(e)
        else:
            try:
                if int(dict_data[str(i)]["Price"].split(".")[0].replace(",", "")) > int(price_range[1:]):
                    for k, v in dict_data[str(i)].items():
                        if k == "Url":
                            make_string += f"<div class='sd-main' >{c})<br/><i> {k} :</i> <a href='{v}'>{v}</a><br/><br/>"
                            c += 1
                        else:
                            make_string += f"<i>{k} : </i>{v}<br/><br/>"
                    make_string += "</div>"
            except ValueError as e:
                print(e)

make_string += """
</div>
</body>
</html>
"""

send_mail(host_name="smtp-relay.sendinblue.com", smtp_id=os.environ.get("Email"), smtp_pass=os.environ.get("Email_pass")
          , to_email=["sdankhara1@gmail.com"], html_contact=make_string)
