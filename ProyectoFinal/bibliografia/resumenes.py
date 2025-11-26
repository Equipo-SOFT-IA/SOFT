# bibliografia/resumenes.py

import os

CARPETA_RESUMENES = "libros_resumen"
os.makedirs(CARPETA_RESUMENES, exist_ok=True)


# ------------------------------------------------------------
# 📥 Guardar texto en la biblioteca
# ------------------------------------------------------------
def guardar_en_bibliografia(nombre, texto):
    """
    Guarda un texto asociado a un nombre dentro de la carpeta libros_resumen.
    El archivo se guarda como .txt
    """
    ruta = os.path.join(CARPETA_RESUMENES, f"{nombre}.txt")

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        return True
    except Exception as e:
        print("Error guardando resumen:", e)
        return False


# ------------------------------------------------------------
# 📚 Cargar todos los textos de la biblioteca
# ------------------------------------------------------------
def cargar_resumenes():
    """
    Lee todos los archivos .txt dentro de libros_resumen
    y devuelve una lista de diccionarios:
    [
        {"nombre": "archivo1.txt", "texto": "..."},
        {"nombre": "archivo2.txt", "texto": "..."},
        ...
    ]
    """
    lista = []

    for archivo in os.listdir(CARPETA_RESUMENES):
        if not archivo.endswith(".txt"):
            continue

        ruta = os.path.join(CARPETA_RESUMENES, archivo)

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            lista.append({
                "nombre": archivo,
                "texto": contenido
            })
        except:
            # Si un archivo está corrupto, lo ignoramos
            continue

    return lista


# ------------------------------------------------------------
# 🔍 Obtener un texto específico por nombre
# ------------------------------------------------------------
def obtener_resumen(nombre):
    """
    Devuelve el contenido de un archivo específico nombre.txt
    o None si no existe.
    """
    ruta = os.path.join(CARPETA_RESUMENES, f"{nombre}.txt")

    if not os.path.exists(ruta):
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None
