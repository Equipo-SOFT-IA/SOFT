# bibliografia/fragmentos.py

from difflib import SequenceMatcher

def buscar_fragmentos(texto_usuario, resumenes, top_n=6):
    """
    Compara el texto del usuario contra todos los textos de la biblioteca.
    
    resumenes debe ser una lista de:
    [
        {"nombre": "archivo.txt", "texto": "..."},
        ...
    ]

    Devuelve los top_n fragmentos con mayor similitud.
    Cada elemento devuelto tiene el formato:
        (score_similitud, nombre_archivo, texto)
    """

    resultados = []

    # Evitamos errores si no hay resumenes
    if not resumenes:
        return []

    texto_usuario = texto_usuario.lower()

    for r in resumenes:
        texto_resumen = r["texto"].lower()

        similitud = SequenceMatcher(
            None,
            texto_usuario,
            texto_resumen
        ).ratio()

        resultados.append((similitud, r["nombre"], r["texto"]))

    # Se ordenan por similitud (de mayor a menor)
    resultados.sort(key=lambda x: x[0], reverse=True)

    # Regresamos solo los más relevantes
    return resultados[:top_n]
