# archivos/imagen.py

from PIL import Image
import io

def cargar_imagen(archivo_stream):
    
    #Carga una imagen desde un archivo subido en Streamlit.
    #Devuelve el objeto PIL.Image
    try:
        contenido = archivo_stream.read()

        # Abrimos la imagen desde bytes
        img = Image.open(io.BytesIO(contenido))

        # Aseguramos que se pueda convertir, así detectamos errores
        img.verify()

        # Reabrimos la imagen ya verificada
        img = Image.open(io.BytesIO(contenido))

        return {
            "tipo": "imagen",
            "imagen": img
        }

    except Exception as e:
        return {
            "tipo": "error",
            "mensaje": f"Error al cargar la imagen: {str(e)}"
        }
