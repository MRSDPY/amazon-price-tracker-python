import bs4 as bs
import requests
import random


class Proxy:
    def __init__(self):
        self.proxies = []
        self.get_free_proxies()
        self.session_n = ""
        self.proxy_n = ""

    def get_free_proxies(self):
        url = "https://sslproxies.org/"

        soup = bs.BeautifulSoup(requests.get(url).content, "html.parser")

        for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                host = f"{ip}:{port}"
                self.proxies.append(host)
            except IndexError:
                continue

    def get_session(self, methods_, url_, headers_):
        while True:
            try:
                proxy = {"https": random.choice(self.proxies)}
                r = requests.request(methods_, url_, proxies=proxy, timeout=5, headers=headers_)
                print("[-] Done")
                break
            except Exception as e:
                print("[?] Error")
                pass
        return r
