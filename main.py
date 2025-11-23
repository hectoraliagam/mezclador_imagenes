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

def nombre_unico_destino(dest_dir, base_name):
    nombre, ext = os.path.splitext(base_name)
    candidato = base_name
    contador = 1
    while os.path.exists(os.path.join(dest_dir, candidato)):
        candidato = f"{nombre}_{contador}{ext}"
        contador += 1
    return candidato

# Función principal
def mezclar_imagenes(config_path='config.json'):
    config = cargar_configuracion(config_path)

    ruta_input = config['ruta_input']
    carpeta_hija_actual = config['carpeta_hija']
    cantidad_por_subcarpeta = config['imagenes_por_subcarpeta']

    # Semilla para trazabilidad
    semilla = datetime.now().timestamp()
    random.seed(semilla)
    logger.info(f"🔁 Semilla aleatoria usada: {semilla}")

    ruta_origen = obtener_ruta_hija(ruta_input, carpeta_hija_actual)
    logger.info(f"📂 Carpeta origen actual: {carpeta_hija_actual:04d}")

    # Crear carpeta destino siguiente
    carpetas_existentes = [
        int(nombre) for nombre in os.listdir(ruta_input)
        if os.path.isdir(os.path.join(ruta_input, nombre)) and nombre.isdigit()
    ]
    siguiente_disponible = max(carpetas_existentes) + 1 if carpetas_existentes else 1
    ruta_destino = obtener_ruta_hija(ruta_input, siguiente_disponible)
    logger.info(f"🗂️ Carpeta destino creada: {siguiente_disponible:04d}")

    subcarpetas = sorted([
        d for d in os.listdir(ruta_origen)
        if os.path.isdir(os.path.join(ruta_origen, d))
    ])
    crear_estructura_destino(ruta_destino, subcarpetas)

    # Construir lista global de imágenes con su subcarpeta de origen
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

    total_unicos_global = len(imagenes_globales)
    logger.info(f"🧮 Imágenes detectadas: {total_unicos_global}")

    # Auditoría: detectar posibles colisiones por nombre (independiente de origen)
    nombres = [i["nombre"] for i in imagenes_globales]
    duplicados_por_nombre = {}
    for n in nombres:
        duplicados_por_nombre[n] = duplicados_por_nombre.get(n, 0) + 1
    colisiones = [n for n, c in duplicados_por_nombre.items() if c > 1]
    if colisiones:
        logger.warning(f"⚠️ Detectadas {len(colisiones)} colisiones de nombre. Se evitarán con renombrado en destino.")

    if total_unicos_global < cantidad_por_subcarpeta:
        mensaje = (
            f"Solo hay {total_unicos_global} imágenes globales, "
            f"pero se requieren {cantidad_por_subcarpeta} por subcarpeta."
        )
        logger.error(mensaje)
        raise ValueError(mensaje)

    # Para cada subcarpeta: tomar un sample SIN REPETICIÓN dentro de la subcarpeta
    # y copiar con nombre único en destino (prefijo de subcarpeta de origen + anti-colisión).
    for sub_dest in subcarpetas:
        ruta_sub_destino = os.path.join(ruta_destino, sub_dest)

        seleccionadas = random.sample(imagenes_globales, cantidad_por_subcarpeta)
        logger.debug(f"🎲 Seleccionadas para {sub_dest}: {[s['nombre'] for s in seleccionadas]}")

        copias_efectivas = 0
        for img in seleccionadas:
            # Prefijo con subcarpeta original para evitar colisiones de nombre
            prefijo = img["subcarpeta_original"]
            base_name = f"{prefijo}__{img['nombre']}"
            destino_final = nombre_unico_destino(ruta_sub_destino, base_name)

            shutil.copy2(
                os.path.join(img["origen"], img["nombre"]),
                os.path.join(ruta_sub_destino, destino_final)
            )
            copias_efectivas += 1

        logger.info(f"✅ Subcarpeta {sub_dest}: {copias_efectivas} imágenes copiadas.")
        # Verificación dura de conteo en disco
        conteo_en_disco = len([
            f for f in os.listdir(ruta_sub_destino)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        if conteo_en_disco != cantidad_por_subcarpeta:
            logger.error(
                f"❌ Verificación: {sub_dest} tiene {conteo_en_disco} archivos, "
                f"debería tener {cantidad_por_subcarpeta}."
            )
        else:
            logger.debug(f"📏 Verificación OK: {sub_dest} tiene {conteo_en_disco}.")

    # Actualizar el número de carpeta hija en el JSON
    config['carpeta_hija'] = carpeta_hija_actual + 1
    guardar_configuracion(config_path, config)
    logger.info(f"🎉 Carpeta {siguiente_disponible:04d} generada exitosamente.")
    logger.info(f"📌 Siguiente carpeta origen: {carpeta_hija_actual + 1:04d}")

if __name__ == "__main__":
    mezclar_imagenes()
