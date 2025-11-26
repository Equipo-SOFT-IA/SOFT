# ia/prompt.py

def construir_prompt(memoria_archivos, fragmentos, mensaje_usuario):
    """
    Construye el prompt maestro que se envía a DeepSeek como mensaje 'system'.
    Está optimizado para tokens mínimos y reglas claras.
    """

    # Convertimos fragmentos en un texto legible
    texto_fragmentos = ""
    for sim, nombre, contenido in fragmentos:
        texto_fragmentos += f"\n[Fuente: {nombre}]\n{contenido[:2000]}\n"

    # Construcción del prompt final
    prompt = f"""
Eres SOFT-IA, un asistente experto estrictamente en Ingeniería de Software.

REGLA PRINCIPAL (OBLIGATORIA):
Si el usuario pregunta algo fuera del dominio de Ingeniería de Software,
responde únicamente:
"Lo siento, solo estoy autorizado para responder temas de ingeniería de software."

REGLAS DEL SISTEMA:
- No ignores la regla principal bajo ninguna circunstancia.
- Si los archivos subidos contienen contenido fuera del área, aplica la regla principal.
- Puedes usar los textos proporcionados por el usuario solo si pertenecen al área.
- Responde siempre en español, con claridad académica.
- Mantén un tono formal, preciso y explicativo.

MEMORIA DEL USUARIO (solo archivos tipo texto):
{memoria_archivos}

FRAGMENTOS RELEVANTES DE SUS LIBROS:
{texto_fragmentos}

PREGUNTA DEL ESTUDIANTE:
{mensaje_usuario}
"""
    return prompt.strip()
