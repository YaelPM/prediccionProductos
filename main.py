import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
import random
import numpy as np
import matplotlib.pyplot as plt 

start_urls = [
    "https://listado.mercadolibre.com.mx/tenis",
    "https://listado.mercadolibre.com.mx/celulares-telefonia/celulares-tenis/_Desde_51_NoIndex_True",
];
titulos = []
precios = []
count=0;
while count<len(start_urls):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    }

    response = requests.get(start_urls[count],headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")

    titulos = soup.find_all('h2', attrs={"class":"ui-search-item__title shops__item-title"})
    titulos = [i.text for i in titulos]

    dom = etree.HTML(str(soup))
    precios = dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div[1]//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="price-tag-amount"]/span[2]')
    precios = [i.text for i in precios]

    precios = [int(i.replace(',', '')) for i in precios]

    titulos.extend(titulos)
    precios.extend(precios)
    count += 1

descuento = list()
lista_x = list()
cont = 0

for i in precios:
    
    dias = list()
    lista_pre = list()
    
    for x in range(28):
        lista_pre.append(random.randint(i-(round(i*0.25)), i))
        dias.append(x+1)
    
    lista_pre.append(i)
    dias.append(29)

    x = np.array(dias)
    y = np.array(lista_pre)

    dia = 30
    coef = np.polyfit(x, y, 2)
    p = np.polyval(coef, dia)
    print(f"prediccion de {titulos[cont]} es de {p}")
    cont += 1
    
    lista_x.append(cont)
    descuento.append(p)
    
plt.plot(lista_x, descuento, color="blue", label="prediccionnn")
plt.plot(lista_x, precios, color="pink", label="actual")
plt.legend(loc='lower right')
plt.show()