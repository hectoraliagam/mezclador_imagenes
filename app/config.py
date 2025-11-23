import json

def cargar_configuracion(ruta_config):
    with open(ruta_config, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def guardar_configuracion(ruta_config, config):
    with open(ruta_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
