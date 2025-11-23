# app/paths.py

import os

def obtener_ruta_hija(ruta_input, numero):
    return os.path.join(ruta_input, f"{numero:04d}")

def crear_estructura_destino(ruta_destino, subcarpetas):
    os.makedirs(ruta_destino, subcarpetas)
    for sub in subcarpetas:
        os.makedirs(os.path.join(ruta_destino, sub), exist_ok=True)
