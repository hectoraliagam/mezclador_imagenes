import os
import shutil

def nombre_unico_destino(dest_dir, base_name):
    nombre, ext = os.path.splitext(base_name)
    candidato = base_name
    contador = 1
    while os.path.exists(os.path.join(dest_dir, candidato)):
        candidato = f"{nombre}_{contador}{ext}"
        contador += 1
    return candidato

def copiar_imagen(origen, destino):
    shutil.copy2(origen, destino)
