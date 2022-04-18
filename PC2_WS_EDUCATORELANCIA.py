# Webscraping a EL PAIS
#
# Se usa BeatifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json

paginas = 10
driver = webdriver.Chrome(ChromeDriverManager().install())

def webscraping():
    listaNoticias = []
    pagina = 1
    while(pagina <= paginas):
        url="https://www.educatolerancia.com/categoria/acoso-escolar/page/"+str(pagina)+"/"
        driver.get(url)
        obtenerNoticias(listaNoticias)
        pagina += 1
    saveJSON(listaNoticias)

def obtenerNoticias(listaNoticias):
    html = driver.find_element(By.XPATH, '//*[@id="content"]/div')
    noticias = html.find_elements(By.TAG_NAME, 'article')
    for noticia in noticias:

        #Obtener la URL
        url = noticia.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        # A partir se usa beatifulSoup para cada noticia de la URL
        r=requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Titulo de la noticia
        titulo = soup.find('h1').string
        # print(titulo)

        # Parrafos
        listaParrafos = []
        container = soup.find('div', class_='entry-content clearfix')
        parrafos = container.find_all('p')
        for parrafo in parrafos:
            if parrafo:
                listaParrafos.append(parrafo.string)
        listaNoticias.append({
            'titulo': titulo,
            'URL': url,
            'Cuerpo': listaParrafos
        })

def saveJSON(listaNoticias):
    with open('Noticias_EDUCATOLERANCIA.json', 'w', encoding='utf-8') as f:
        json.dump(listaNoticias, f, ensure_ascii=False)

webscraping()