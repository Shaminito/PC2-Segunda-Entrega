# Webscraping a Google Maps
#
# Correo: pc2uem@gmail.com
# Contraseña: Qwerty1234@
#
# No se usa BeatifulSoup

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
url="https://www.google.es/maps/"

def webscraping(query):
    driver.get(url)
    aceptarCookies()
    iniciarSesion()
    introducirQuery(query)
    listaURL = todosColegios()
    listaColegios = obtenerOpiniones(listaURL)
    # print(listaColegios)
    saveJSON(listaColegios)


def aceptarCookies():
    driver.find_element_by_class_name("VfPpkd-LgbsSe").click()

def iniciarSesion():
    # Introducir Correo
    inputCorreo = driver.find_element_by_class_name("whsOnd")
    inputCorreo.send_keys("pc2uem@gmail.com")
    driver.find_element_by_class_name("VfPpkd-LgbsSe").click()

    # Esperar a que este lista el input de la contraseña
    time.sleep(2)

    # Introducir Contraseña
    inputContrasenya = driver.find_element(By.CLASS_NAME, "whsOnd")
    inputContrasenya.send_keys("Qwerty1234@")
    driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe").click()

    # Esperar a que salga el mapa

    time.sleep(1)

def introducirQuery(query):
    driver.find_element(By.ID, 'searchboxinput').send_keys(query)

    driver.find_element(By.ID, 'searchbox-searchbutton').click()
    
    # Esperar a que salga los resultados
    time.sleep(5)

def todosColegios():
    listaURL = []
    # Seleccionar el colegio de la lista

    colegios_xpath = '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/*'
    colegios = driver.find_elements(By.XPATH, colegios_xpath)

    for colegio in colegios:
        try:
            url_colegio = colegio.find_element(By.TAG_NAME,'a').get_attribute('href')
            listaURL.append(url_colegio)
        except NoSuchElementException:
            pass
    return listaURL

def obtenerOpiniones(listaURL):
    listaColegios = []
    for url in listaURL:
        driver.get(url)
    
        # A partir de aqui empieza a sacar las reseñas del colegio

        nombre_colegio = driver.find_element(By.TAG_NAME,'h1').text
        #print(nombre_colegio)
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button').click()
        
            time.sleep(5)

            # Obtener lista de opiniones

            opiniones = driver.find_elements(By.CLASS_NAME, 'siAUzd-neVct')

            listaOpiniones = []
            for opinion in opiniones:
                try:
                    opinion_text = opinion.find_element(By.CLASS_NAME, 'ODSEW-ShBeI-text').text
                    listaOpiniones.append(opinion_text)
                except NoSuchElementException as e:
                    pass
            # print(listaOpiniones)
            listaColegios.append({
                'colegio':nombre_colegio, 
                'url':url,
                'opiniones': listaOpiniones
                })
        except NoSuchElementException:
            pass
    return listaColegios

def saveJSON(listaColegios):
    # print(listaColegios)
    with open('colegios.json', 'w', encoding='utf-8') as f:
        json.dump(listaColegios, f, ensure_ascii=False)

# EJECUCION
webscraping('Colegio')