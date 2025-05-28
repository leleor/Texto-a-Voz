# Este programa se puede actualizar solo.
# Comprobará si hay una versión más reciente subida a internet.
# Si la hay, se actualizará automáticamente y te pedirá que lo abras de nuevo.

import os
import requests
import hashlib

# Dirección de internet donde está guardada la última versión del archivo
# 💡 CAMBIA esta dirección por la tuya real
URL_DEL_ARCHIVO = 'https://raw.githubusercontent.com/USUARIO/REPO/main/lector.py'

# Esta parte localiza el archivo que estás usando ahora mismo
archivo_local = os.path.abspath(__file__)

# Esta función crea un "resumen" del texto para compararlo fácilmente
def calcular_resumen(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

# Esta parte comprueba si hay una versión nueva del archivo en internet
def comprobar_y_actualizar():
    try:
        respuesta = requests.get(URL_DEL_ARCHIVO)
        if respuesta.status_code == 200:
            version_en_internet = respuesta.text

            with open(archivo_local, 'r', encoding='utf-8') as f:
                version_en_tu_ordenador = f.read()

            # Comparamos las dos versiones
            if calcular_resumen(version_en_internet) != calcular_resumen(version_en_tu_ordenador):
                print("🔄 Se ha encontrado una versión nueva. Actualizando...")
                with open(archivo_local, 'w', encoding='utf-8') as f:
                    f.write(version_en_internet)
                print("✅ El programa se ha actualizado. Ábrelo de nuevo.")
                exit()
            else:
                print("✔️ El programa ya está actualizado.")
        else:
            print("⚠️ No se pudo comprobar si hay actualizaciones. (Código:", respuesta.status_code, ")")
    except Exception as e:
        print("❌ Ha ocurrido un error al buscar actualizaciones:", e)

# Primero comprobamos si hay una versión nueva
comprobar_y_actualizar()

from gtts import gTTS
import PyPDF2

# Esta parte hace que el programa trabaje en la misma carpeta donde está guardado
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Pedimos al usuario que escriba el nombre del archivo a leer
nombre_archivo = input("Introduce el nombre del archivo (por ejemplo, archivo.pdf): ").strip()

# Detectamos la extensión (tipo) del archivo
_, extension = os.path.splitext(nombre_archivo)
extension = extension.lower()

texto = ""

try:
    if extension == ".txt":
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
    elif extension == ".pdf":
        with open(nombre_archivo, 'rb') as f:
            lector = PyPDF2.PdfReader(f)
            for pagina in lector.pages:
                texto += pagina.extract_text()
    else:
        print("❌ Tipo de archivo no válido. Usa un archivo .txt o .pdf.")
        input("Pulsa Enter para salir...")
        exit()

    # Convertimos el texto a voz (audio)
    tts = gTTS(text=texto, lang='es')
    tts.save("audio.mp3")
    print("✅ Se ha creado el archivo de audio 'audio.mp3'.")
except Exception as e:
    print(f"❌ Ha ocurrido un error: {e}")

input("Pulsa Enter para salir...")
