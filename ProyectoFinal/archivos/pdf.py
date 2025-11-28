# archivos/pdf.py

import fitz  # PyMuPDF

def procesar_pdf(archivo_stream):

    #Procesa un archivo PDF subido desde Streamlit.
    #Devuelve el texto extraído de todas las páginas.
    try:
        # Abrir el PDF desde el stream cargado
        doc = fitz.open(stream=archivo_stream.read(), filetype="pdf")

        texto = ""
        for pagina in doc:
            texto += pagina.get_text()

        return texto if texto.strip() else "(PDF sin texto detectable)"

    except Exception as e:
        return f"(Error procesando PDF: {str(e)})"
