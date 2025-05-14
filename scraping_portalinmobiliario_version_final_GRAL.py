from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import re
from datetime import datetime
import os
import random
import unicodedata

# Ruta para guardar archivos
OUTPUT_DIR = r"C:/Users/sebos/Desktop/scrapping/PORTAL INMOBILIARIO/Resultados"


# === Normalización de texto ===
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.replace(" ", "-").replace("ñ", "n")
    return texto



def convertir_a_clp(precio_str, uf_value):
    if "UF" in precio_str:
        match = re.search(r"[\d,.]+", precio_str)
        if match:
            uf_valor = float(match.group(0).replace(".", "").replace(",", "."))
            return round(uf_valor * uf_value)
    elif "$" in precio_str:
        match = re.search(r"[\d.]+", precio_str)
        if match:
            return int(match.group(0).replace(".", ""))
    return None


#----SCRAPPER


def scrapear_combinacion(op,tip,reg,com,dorm,UF, chromedriver_path="chromedriver.exe"):
    url = f"https://www.portalinmobiliario.com/{op}/{tip}/{dorm}/{com}-{reg}"
    print(f"🔍 Scrapeando: {op}|{tip}|{reg}|{com}| {dorm}")
    # === CONFIGURACIÓN SELENIUM ===
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logfile = open(f"log_scraping_{timestamp}.txt", "w", encoding="utf-8")
    def log(msg):
        print(msg)
        logfile.write(msg + "\n")


    propiedades = []
    pagina_actual = 1
    total_propiedades = 0

    try:
        driver.get(url)
        tiempo_espera = random.uniform(3, 7)
        time.sleep(tiempo_espera)
        while True:
            log(f"🔄 Procesando página {pagina_actual}...")
            cards = driver.find_elements(By.CSS_SELECTOR, "div.andes-card.andes-card--flat.andes-card--animated")
            log(f"🔍 Se encontraron {len(cards)} tarjetas.")
            props_pagina = 0
            for card in cards:
                try:
                    titulo = card.find_element(By.CSS_SELECTOR, 'a.poly-component__title').text
                    link = card.find_element(By.CSS_SELECTOR, 'a.poly-component__title').get_attribute('href')
                    precio = card.find_element(By.CSS_SELECTOR, 'div.poly-component__price').text.strip()
                    # Dentro de esa tarjeta, buscar los ítems de atributos
                    atributos = card.find_elements(By.CSS_SELECTOR, "ul.poly-attributes-list li")
                    # Extraer texto uno por uno
                    atributos_texto = [a.text.strip() for a in atributos]
                    dormitorios = atributos_texto[0]
                    banios = atributos_texto[1]
                    metros=atributos_texto[2]
                    try:
                        ubicacion = card.find_element(By.CSS_SELECTOR, 'span.poly-component__location').text
                    except:
                        ubicacion = None
                    try:
                        entrega = card.find_element(By.CSS_SELECTOR, 'span.poly-component__possession-date').text
                    except:
                        entrega = None
                    try:
                        disponibles = card.find_element(By.CSS_SELECTOR, 'span.poly-component__available-units').text
                    except:
                        disponibles = None

                    precio_clp = convertir_a_clp(precio,UF) 

                    propiedades.append({
                        "Link": link,
                        "Comuna":  com,
                        "Propiedad": titulo,
                        "Tipo": tip,
                        "precio": precio,
                        "precio_CLP": precio_clp,
                        "Ubicación": ubicacion,
                        "Dormitorios" :dormitorios,
                        "Baños": banios,
                        "Metros" : metros,
                        "Entrega" : entrega,
                        "Disponibles" : disponibles
                    })
                    props_pagina += 1
                except Exception as e:
                    log(f"⚠️ Error al procesar tarjeta: {str(e)}")
                    continue

            total_propiedades += props_pagina
            log(f"✅ Página {pagina_actual} procesada: {props_pagina} propiedades registradas. Total acumulado: {total_propiedades}")


            try:
                siguiente_pagina = pagina_actual + 1
                xpath_num_pagina = f"//a[contains(@aria-label, 'Ir a la página {siguiente_pagina}')]"
            
                wait = WebDriverWait(driver, 10)
                numero_pagina = wait.until(EC.presence_of_element_located((By.XPATH, xpath_num_pagina)))
            
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", numero_pagina)
                time.sleep(random.uniform(1.5, 2.5))
            
                numero_pagina.click()
                print(f"✅ Avanzando a página {siguiente_pagina}")
                pagina_actual += 1
                time.sleep(random.uniform(3, 5))
            
            except TimeoutException:
                print("🔴 No hay más números de página.")
                break
        return propiedades
    finally:
        driver.quit()
        

# === Listas válidas para filtros ===
tipos_validos = ["departamento", "casa", "oficina", "local"]

regiones_validas = ["Antofagasta", "Atacama", "Coquimbo", "Valparaíso", "Metropolitana",
    "bernardo ohiggins", "Maule", "Ñuble", "Biobío", "La Araucanía",
    "Los Ríos", "Los Lagos", "Aysén", "Magallanes", "Tarapacá"]

dormitorios_validos = ["Monoambiente", "1 dormitorio", "2 dormitorios", "3 dormitorios", "más de 4 dormitorios"]

# banos_validos = {"1 baño": "_Banos_1",
#                  "2 baños": "_Banos_2",
#                  "3 baños": "_Banos_3",
#                  "4 baños": "_Banos_4",
#                  "5 baños o más": "_Banos_5-o-mas"}



## Función para mostrar opciones y obtener input como lista de índices
def seleccionar_opciones(lista, nombre="opción"):
    print(f"\nSelecciona {nombre}(es):")
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")
    seleccion = input("Ingresa los números separados por coma (ej: 1,3): ")
    indices = [int(i.strip()) - 1 for i in seleccion.split(",") if i.strip().isdigit()]
    return [lista[i] for i in indices if 0 <= i < len(lista)]

# Inputs de usuario
print("Bienvenido procesa a ingresar sus filtros")
uf = float(input("Ingrese valor actual de la UF en CLP sin puntos:"))
operaciones = seleccionar_opciones(["venta", "arriendo"], "operación")
tipos = seleccionar_opciones(tipos_validos, "tipo de inmueble")
regiones = seleccionar_opciones(regiones_validas, "región")
comunas_raw = input("Ingresa comunas separadas por coma (ej: Ñuñoa, Las Condes): ").split(",")
comunas = [normalizar(c.strip()) for c in comunas_raw if c.strip()]
dormitorios = seleccionar_opciones(dormitorios_validos, "cantidad de dormitorios")

# print("\nOpciones de baños:")
# banos_keys = list(banos_validos.keys())
# for i, b in enumerate(banos_keys, start=1):
#     print(f"{i}. {b}")
# banos_seleccion = input("Selecciona número(s) separados por coma (ej: 2,3): ")
# banos_indices = [int(i.strip()) - 1 for i in banos_seleccion.split(",") if i.strip().isdigit()]
# banos = [banos_validos[banos_keys[i]] for i in banos_indices if 0 <= i < len(banos_keys)]

# === Construcción de 2URL ===
for operacion in operaciones:
    for tipo in tipos:
        tipo = normalizar(tipo)
        for region in regiones:
            region = normalizar(region)
            for comuna in comunas:
                comuna = normalizar(comuna)
                for dormitorio in dormitorios:
                    dormitorio  = normalizar(dormitorio)
                   # for bano in banos:
                    resultados = scrapear_combinacion(operacion,tipo,region,comuna, dormitorio,uf)
                    if resultados:
                            df = pd.DataFrame(resultados)
                            nombre = f"resultados_{operacion}_{tipo}_{region.replace(' ','')}_{comuna.replace(' ', '')}_{tipo}_{dormitorio.replace(' ', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                            ruta = os.path.join(OUTPUT_DIR, nombre)
                            df.to_csv(ruta, index=False, encoding="utf-8-sig")
                            print(f"✅ Guardado {len(df)} propiedades en {nombre}")
                    else:
                            print(f"⚠️ Sin resultados válidos para {operacion}|{tipo}|{region}|{comuna}| {dormitorio} ")
print("\\n🔗 Enlaces generados:")
                        



                

