
import requests
from bs4 import BeautifulSoup

url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_gid=GA1.2.554329263.1745330196; _ga_DJLCSW50SC=GS1.1.1745339071.2.1.1745339074.57.0.0; _ga_D6NF5QC4QT=GS1.1.1745339071.2.1.1745339075.56.0.0; _ga=GA1.2.1606191101.1745330193; FCNEC=%5B%5B%22AKsRol80Dc4w1rYolqyR4xdS708rzCBVVM-yPyAWZySW6MA7dma3eHrbog2MUU8N-GlOwvu6ajM2LozhaJdQx1QSirRTOJQLJ95l2yWrNu7KJ4yfgG4OfS9ZRkTmDcHj89IM7f6vd_VLGPoGxvJ7uG6mLr3C8N669g%3D%3D%22%5D%5D',
}

resp = requests.get(url, headers=headers)

soup = BeautifulSoup(resp.text, "html.parser")
div = soup.find("div" , class_='td-page-content')

paragrafo = div.find_all("p")[1]

print(paragrafo.find_all("em"))