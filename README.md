# Mezclador de Imágenes

Este proyecto permite **mezclar imágenes desde una carpeta origen hacia
una carpeta destino**, distribuyéndolas aleatoriamente y manteniendo una
estructura organizada por subcarpetas.\
Cada ejecución crea automáticamente una nueva carpeta con las imágenes
mezcladas, evitando colisiones de nombres y actualizando el progreso en
`config.json`.

------------------------------------------------------------------------

## 🚀 Características

-   Lectura automática de configuración (`config.json`)
-   Detección de carpetas numéricas (`0001`, `0002`, ...)
-   Mezcla global de imágenes sin repetición por subcarpeta
-   Creación automática de carpetas destino
-   Renombrado inteligente para evitar colisiones
-   Logs detallados mediante `logger.py`
-   Ejecución simple con `run.bat`

------------------------------------------------------------------------

## 📂 Estructura del Proyecto

    project/
    │
    ├─ app/
    │   ├─ config.py
    │   ├─ paths.py
    │   ├─ file_ops.py
    │   ├─ mixer.py
    │   └─ logger.py
    │
    ├─ main.py
    ├─ config.json
    └─ run.bat

------------------------------------------------------------------------

## ⚙️ Configuración (`config.json`)

Ejemplo:

``` json
{
    "ruta_input": "C:/Rutas/Imagenes",
    "carpeta_hija": 1,
    "imagenes_por_subcarpeta": 50
}
```

### Campos:

-   **ruta_input**\
    Ruta base donde se encuentran las carpetas numeradas (`0001`,
    `0002`, etc.)

-   **carpeta_hija**\
    Indica qué carpeta será tomada como origen en la próxima ejecución.\
    El programa lo incrementa automáticamente.

-   **imagenes_por_subcarpeta**\
    Cantidad de imágenes que se copiarán a cada subcarpeta destino.

------------------------------------------------------------------------

## ▶️ Ejecución en Windows

Simplemente haz doble clic en **run.bat**:

    run.bat

Este script:

-   Activa el entorno virtual `.venv`
-   Ejecuta `main.py`
-   Muestra el resultado en la consola

------------------------------------------------------------------------

## 🔧 Ejecución manual (opcional)

Si deseas ejecutarlo sin el `.bat`:

``` bash
.\.venv\Scripts\activate
python main.py
```

------------------------------------------------------------------------

## 📝 Logs

El proyecto genera logs con información como:

-   Semilla usada para aleatoriedad\
-   Carpeta origen y destino\
-   Cantidad de imágenes detectadas\
-   Imágenes seleccionadas para cada subcarpeta\
-   Verificación final de copias

Útil para auditoría o depuración.

------------------------------------------------------------------------

## 📌 Notas Importantes

-   El script **solo procesa imágenes** `.jpg`, `.jpeg`, `.png`
-   Los nombres duplicados entre subcarpetas se manejan automáticamente
-   Si hay menos imágenes globales que las requeridas, se detendrá con
    error
-   Cada ejecución crea una nueva carpeta destino incremental

------------------------------------------------------------------------

## 👨‍💻 Autor

**Hector Aliaga**\
GitHub: https://github.com/hectoraliagam\
Contacto: aliagamdnhectorgbl@gmail.com

------------------------------------------------------------------------

## 📄 Licencia

Uso personal o empresarial permitido.\
No redistribuir sin permiso del autor.
