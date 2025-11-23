import os
import random
from datetime import datetime
from app.logger import setup_logger
from app.config import cargar_configuracion, guardar_configuracion
from app.paths import obtener_ruta_hija, crear_estructura_destino
from app.file_ops import nombre_unico_destino, copiar_imagen

logger = setup_logger(__name__)

def obtener_subcarpetas(ruta):
    return sorted([
        d for d in os.listdir(ruta)
        if os.path.isdir(os.path.join(ruta, d))
    ])
    
def recolectar_imagenes(ruta_origen, subcarpetas):
    imagenes = []
    for sub in subcarpetas:
        ruta_sub = os.path.join(ruta_origen, sub)
        for img in os.listdir(ruta_sub):
            if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                imagenes.append({
                    "nombre": img,
                    "origen": ruta_sub,
                    "subcarpeta_original": sub
                })
    return imagenes

def detectar_colisiones(imagenes):
    nombres = [i["nombre"] for i in imagenes]
    duplicados = {}
    for n in nombres:
        duplicados[n] = duplicados.get(n, 0) + 1
    return [n for n, c in duplicados.items() if c > 1]

def mezclar_imagenes(config_path="config.json"):
    config = cargar_configuracion(config_path)
    
    ruta_input = config['ruta_input']
    carpeta_hija_actual = config['carpeta_hija']
    cantidad_por_subcarpeta = config['imagenes_por_subcarpeta']
    
    # Semilla
    semilla = datetime.now().timestamp()
    random.seed(semilla)
    logger.info(f"Semilla usada: {semilla}")
    
    ruta_origen = obtener_ruta_hija(ruta_input, carpeta_hija_actual)
    logger.info(f"Carpeta origen: {carpeta_hija_actual:04d}")
    
    # Crear carpeta destino autoincrementada
    carpetas_existentes = [
        int(nombre) for nombre in os.listdir(ruta_input)
        if os.path.isdir(os.path.join(ruta_input, nombre)) and nombre.isdigit()
    ]
    siguiente_disponible = max(carpetas_existentes) + 1 if carpetas_existentes else 1
    ruta_destino = obtener_ruta_hija(ruta_input, siguiente_disponible)
    logger.info(f"Carpeta destino: {siguiente_disponible:04d}")
    
    subcarpetas = obtener_subcarpetas(ruta_origen)
    crear_estructura_destino(ruta_destino, subcarpetas)
    
    imagenes_globales = recolectar_imagenes(ruta_origen, subcarpetas)
    total = len(imagenes_globales)
    logger.info(f"Total imágenes detectadas: {total}")
    
    if total < cantidad_por_subcarpeta:
        raise ValueError(
            f"Solo hay {total} imágenes globales, "
            f"pero se requieren {cantidad_por_subcarpeta} por subcarpeta."
        )
        
    # Colisiones de nombre
    colisiones = detectar_colisiones(imagenes_globales)
    if colisiones:
        logger.warning(f"Colisiones detectadas: {len(colisiones)}")
        
    # Mezclar y copiar
    for sub_dest in subcarpetas:
        ruta_sub_destino = os.path.join(ruta_destino, sub_dest)
        seleccionadas = random.sample(imagenes_globales, cantidad_por_subcarpeta)
        
        for img in seleccionadas:
            prefijo = img["subcarpeta_original"]
            base = f"{prefijo}__{img['nombre']}"
            destino_final = nombre_unico_destino(ruta_sub_destino, base)
            
            copiar_imagen(
                os.path.join(img['origen'], img['nombre']),
                os.path.join(ruta_sub_destino, destino_final)
            )
            
        logger.info(f"{sub_dest}: {cantidad_por_subcarpeta} imágenes copiadas.")
        
    # Actualizar JSON
    config['carpeta_hija'] = carpeta_hija_actual + 1
    guardar_configuracion(config_path, config)
    
    logger.info("Proceso completado.")
    logger.info(f"Siguiente carpeta origen: {carpeta_hija_actual + 1:04d}")
