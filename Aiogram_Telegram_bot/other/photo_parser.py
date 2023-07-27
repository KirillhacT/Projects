# import requests
# from bs4 import BeautifulSoup
#
# url = "https://www.yandex.ru/images/search?from=tabbar&text=%D0%A5%D0%BE%D1%80%D0%B2%D0%B0%D1%82%D0%B8%D1%8F"
# class_item = "serp-item__thumb justifier__thumb"
#
# req = requests.get(url)
# soup = BeautifulSoup(req.text, "lxml")
#
# elements = soup.find_all(class_=class_item)
# norm_el = []
# for el in elements:
#     src = el.get("src")
#     norm_el.append(f"https:{src}")
# print(norm_el)
# with open("photos.txt", "w", encoding="utf-8") as file:
#     for i in norm_el:
#         file.write(i + "\n")

