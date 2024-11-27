import os
import pdb

import requests
from bs4 import BeautifulSoup

# Base URL del sitio web
BASE_URL = "https://www.acordes.lacuerda.net"

# Nombre del artista
ARTISTA = "vela_puerca"  # Usar formato del sitio, reemplazar espacios por "_"

# Ruta local para guardar canciones
CARPETA_DESCARGAS = "canciones_lacuerda"

# Función para obtener la lista de canciones del artista
def obtener_lista_canciones():
    #pdb.set_trace()  #DEBUGGER DE PYTHON
    url_artista = f"{BASE_URL}/{ARTISTA}/"
    print(f"Obteniendo canciones desde: {url_artista}")
    respuesta = requests.get(url_artista)
    
    print(f"Respuesta SATUS CODE: {respuesta.status_code}")
    if respuesta.status_code != 200:
        print("Error al acceder a la página del artista.")
        return []
    
    return obtener_enlaces_canciones(respuesta)

def obtener_enlaces_canciones(respuesta):
    if respuesta.status_code != 200:
        print(f"Error al obtener la página: {respuesta.status_code}")
        return []

    soup = BeautifulSoup(respuesta.text, "html.parser")
    # Identificar los enlaces a las canciones (puede variar según la estructura del sitio)
    enlaces_canciones = soup.find_all("a", href=True)
    print(f"Enlaces encontrados: {len(enlaces_canciones)}")

    canciones = [
        enlace['href']
        for enlace in enlaces_canciones
        if ARTISTA not in enlace["href"] and "video" not in enlace["href"] and "/tabs/" not in enlace["href"] and not enlace['href'].startswith("javascript:")
    ]
    print(f"Canciones filtradas: {len(canciones)}")
    return canciones

# Función para descargar una canción
def descargar_cancion(url):
    url_artista = f"{BASE_URL}/{ARTISTA}/"
    print(f"Descargando canción desde: {url_artista}{url}")
    try:
        respuesta = requests.get(url_artista + url)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la canción: {url} - {e}")
        return
    
    try:
        soup = BeautifulSoup(respuesta.text, "html.parser")
        contenido = soup.find("pre")  # Generalmente el contenido de acordes está en un <pre>
        
        if not contenido:
            print("No se encontró contenido en esta página.")
            return
        
        titulo = url.split("/")[-1].replace(".html", "")
        archivo = os.path.join(ARTISTA, f"{titulo}.txt")
        
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido.text)
        
        print(f"Canción guardada: {archivo}")
    except Exception as e:
        print(f"Error procesando la canción: {url} - {e}")

# Función principal
def main():
    if not os.path.exists(CARPETA_DESCARGAS):
        os.makedirs(CARPETA_DESCARGAS)
    if not os.path.exists(ARTISTA):
        os.makedirs(ARTISTA)
    canciones = obtener_lista_canciones()
    print(f"Se encontraron {len(canciones)} canciones.")
    
    for url_cancion in canciones:
        descargar_cancion(url_cancion)

if __name__ == "__main__":
    main()
