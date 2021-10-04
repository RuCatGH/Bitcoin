import requests
from bs4 import BeautifulSoup
import time


class Currency:
    url = 'https://www.google.ru/search?q=биткоин+курс+к+доллару&newwindow=1&ei=-eLVYJfGNq_5qwGQ-oWYBQ&oq=биткоин+&gs_lcp=Cgdnd3Mtd2l6EAMYADIJCAAQQxBGEIICMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgIIADICCAA6CAguEMcBEKMCOgoILhDHARCjAhBDOggIABAKEAEQQzoICAAQChABECo6BggAEAoQAToKCAAQ6gIQtAIQQzoHCAAQRhCCAjoCCC46BAguEEM6BAgAEApKBAhBGABQj-EGWM-AB2CgkgdoA3ACeACAAasBiAGrD5IBBDAuMTSYAQCgAQGqAQdnd3Mtd2l6sAEKwAEB&sclient=gws-wiz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36'}
    diferent = 1
    compare_currency = 0

 # init
    def __init__(self):
        self.compare_currency = float(self.get_currency())

# get currency bitcoin
    def get_currency(self):
        full_page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll(
            "span", {"class": "DFlfde SwHCTb"})
        return (convert[0].text).replace(",", "")

# compare and conclusion
    def check_currency(self):
        price = float(self.get_currency())
        if price >= self.compare_currency + self.diferent:
            print("Цена биткоина выросла.")
        elif price <= self.compare_currency - self.diferent:
            print("Цена биткоина упала.")
            
        print(str(price))
        time.sleep(3)
        self.check_currency()
        

