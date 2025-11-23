# main.py

import os
import json
import shutil
import random
from datetime import datetime
from logger import setup_logger


logger = setup_logger(__name__)

# Cargar configuración desde config.json
def cargar_configuracion(ruta_config):
    with open(ruta_config, 'r', encoding='utf-8') as f:
        return json.load(f)
    
# Guardar configuración actualizada en config.json
def guardar_configuracion(ruta_config, config):
    with open(ruta_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        
# Obtener ruta completa de carpeta hija
def obtener_ruta_hija(ruta_input, numero):
    return os.path.join(ruta_input, f"{numero:04d}")

# Crear estructura de carpeta hija destino
def crear_estructura_destino(ruta_destino, subcarpetas):
    os.makedirs(ruta_destino, exist_ok=True)
    for sub in subcarpetas:
        os.makedirs(os.path.join(ruta_destino, sub), exist_ok=True)


# Función principal
def mezclar_imagenes(config_path='config.json'):
    config = cargar_configuracion(config_path)
        
    ruta_input = config['ruta_input']
    carpeta_hija_actual = config['carpeta_hija']
    cantidad_por_subcarpeta = config['imagenes_por_subcarpeta']
    
    semilla = datetime.now().timestamp()
    random.seed(semilla)
    logger.info(f"🔁 Semilla aleatoria usada: {semilla}")
    
    ruta_origen = obtener_ruta_hija(ruta_input, carpeta_hija_actual)
    logger.info(f"📂 Carpeta origen actual: {carpeta_hija_actual:04d}")
    
    carpetas_existentes = [
        int(nombre) for nombre in os.listdir(ruta_input)
        if os.path.isdir(os.path.join(ruta_input, nombre)) and nombre.isdigit()
    ]
    siguiente_disponible = max(carpetas_existentes) + 1
    ruta_destino = obtener_ruta_hija(ruta_input, siguiente_disponible)
    logger.info(f"🗂️ Carpeta destino creada: {siguiente_disponible:04d}")
    
    subcarpetas = sorted([d for d in os.listdir(ruta_origen) if os.path.isdir(os.path.join(ruta_origen, d))])
    crear_estructura_destino(ruta_destino, subcarpetas)
    
    # Construir lista global de imágenes
    imagenes_globales = []
    for sub in subcarpetas:
        ruta_sub_origen = os.path.join(ruta_origen, sub)
        for img in os.listdir(ruta_sub_origen):
            if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                imagenes_globales.append({
                    "nombre": img,
                    "origen": ruta_sub_origen,
                    "subcarpeta_original": sub
                })
                
    if len(imagenes_globales) < cantidad_por_subcarpeta:
        mensaje = f"Solo hay {len(imagenes_globales)} imágenes disponibles, pero se requieren al menos {cantidad_por_subcarpeta}."
        logger.warning(f"⚠️ {mensaje}")
        raise ValueError(mensaje)
    
    # Para cada subcarpeta: tomar un sample aleatorio de todas las imágenes
    for sub in subcarpetas:
        ruta_sub_destino = os.path.join(ruta_destino, sub)
        seleccionadas = random.sample(imagenes_globales, cantidad_por_subcarpeta)  # sin repetición
        for img in seleccionadas:
            shutil.copy2(os.path.join(img["origen"], img["nombre"]),
                         os.path.join(ruta_sub_destino, img["nombre"]))
        logger.info(f"✅ Subcarpeta {sub}: {len(seleccionadas)} imágenes copiadas.")
        logger.debug(f"    Imágenes: {[img['nombre'] for img in seleccionadas]}")
        
    # Actualizar el número de carpeta hija en el JSON
    config['carpeta_hija'] = carpeta_hija_actual + 1
    guardar_configuracion(config_path, config)
    logger.info(f"🎉 Carpeta {siguiente_disponible:04d} generada exitosamente.")
    logger.info(f"📌 Siguiente carpeta origen: {carpeta_hija_actual + 1:04d}")

# Ejecutar
if __name__ == "__main__":
    mezclar_imagenes()
