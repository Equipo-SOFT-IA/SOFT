# archivos/docx.py

from docx import Document
import io

def procesar_docx(archivo_stream):

    #Procesa un archivo .docx subido desde Streamlit.
    #Devuelve todo el texto concatenado de sus párrafos.
    try:
        # Convertir el archivo a un buffer de memoria
        buffer = io.BytesIO(archivo_stream.read())
        doc = Document(buffer)

        lineas = [p.text for p in doc.paragraphs]
        texto = "\n".join(lineas)

        return texto if texto.strip() else "(El archivo .docx no contiene texto)"

    except Exception as e:
        return f"(Error procesando archivo .docx: {str(e)})"
