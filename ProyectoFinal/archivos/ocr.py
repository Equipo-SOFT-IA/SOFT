# archivos/ocr.py

import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ruta de Tesseract opcional (puedes ajustarla aquí si quieres dejarlo global)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extraer_texto_ocr(imagen_pil):
    """
    Recibe una imagen PIL y extrae texto usando OCR (español).
    Devuelve un diccionario con el tipo y el texto detectado.
    """
    try:
        if not isinstance(imagen_pil, Image.Image):
            return {
                "tipo": "texto",
                "texto": "(Error: el objeto proporcionado no es una imagen válida)"
            }

        # Intentamos extraer texto en español
        texto = pytesseract.image_to_string(imagen_pil, lang="spa")

        if not texto or not texto.strip():
            return {
                "tipo": "texto",
                "texto": "(No se detectó texto legible en la imagen)"
            }

        return {
            "tipo": "texto",
            "texto": texto.strip()
        }

    except Exception as e:
        return {
            "tipo": "texto",
            "texto": f"(Error procesando OCR: {str(e)})"
        }
