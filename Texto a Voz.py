# ===============================
# 1. INSTALAR LIBRERÍAS SI FALTAN
# ===============================
import subprocess
import sys

librerias_necesarias = ['requests', 'gTTS', 'PyPDF2']
for libreria in librerias_necesarias:
    try:
        __import__(libreria)
    except ImportError:
        print(f"📦 Instalando librería que falta: {libreria}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])

# ===============================
# 2. ACTUALIZACIÓN AUTOMÁTICA
# ===============================
import os
import requests
import hashlib

# Dirección del archivo en GitHub (versión actualizada del programa)
URL_DEL_ARCHIVO = 'https://raw.githubusercontent.com/leleor/Texto-a-Voz/refs/heads/main/Texto%20a%20Voz.py'
archivo_local = os.path.abspath(__file__)

def calcular_resumen(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def comprobar_y_actualizar():
    try:
        respuesta = requests.get(URL_DEL_ARCHIVO)
        if respuesta.status_code == 200:
            version_online = respuesta.text
            with open(archivo_local, 'r', encoding='utf-8') as f:
                version_local = f.read()

            if calcular_resumen(version_online) != calcular_resumen(version_local):
                print("🔄 Se ha encontrado una versión nueva. Actualizando...")
                with open(archivo_local, 'w', encoding='utf-8') as f:
                    f.write(version_online)
                print("✅ El programa se ha actualizado. Ábrelo de nuevo.")
                input("Pulsa Enter para salir...")
                exit()
            else:
                print("✔️ El programa ya está actualizado.")
        else:
            print(f"⚠️ No se pudo comprobar si hay actualizaciones. (Código: {respuesta.status_code})")
    except Exception as e:
        print(f"❌ Error al buscar actualizaciones: {e}")

comprobar_y_actualizar()

# ===============================
# 3. PROGRAMA PRINCIPAL
# ===============================
from gtts import gTTS
import PyPDF2

# Asegura que se trabaje en la carpeta donde está guardado el programa
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Pedimos el nombre del archivo que el usuario quiere convertir a voz
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
                texto_extraido = pagina.extract_text()
                if texto_extraido:
                    texto += texto_extraido
    else:
        print("❌ Tipo de archivo no válido. Usa un archivo .txt o .pdf.")
        input("Pulsa Enter para salir...")
        exit()

    # Convertimos el texto a voz
    tts = gTTS(text=texto, lang='es')
    tts.save("audio.mp3")
    print("✅ Se ha creado el archivo de audio 'audio.mp3'.")
except Exception as e:
    print(f"❌ Ha ocurrido un error: {e}")

input("Pulsa Enter para salir...")
