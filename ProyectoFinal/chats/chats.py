# chats/chats.py

"""
Módulo encargado de manejar la lógica interna del chat:
- Crear nuevos mensajes
- Añadir mensajes al historial actual
- Limpiar o resetear un chat
"""

def crear_mensaje(role, content):
    """
    Crea un mensaje con estructura estándar.
    role: "user" o "assistant"
    content: texto del mensaje
    """
    return {
        "role": role,
        "content": content
    }


def agregar_mensaje(historial, role, content):
    """
    Agrega un mensaje al historial (lista).
    Devuelve el historial actualizado.
    """
    historial.append(crear_mensaje(role, content))
    return historial


def limpiar_chat():
    """
    Devuelve un historial vacío.
    """
    return []


def borrar_ultimo_mensaje(historial):
    """
    Borra el último mensaje del historial.
    Si el historial está vacío, no hace nada.
    """
    if historial:
        historial.pop()
    return historial


def obtener_ultimo_mensaje(historial):
    """
    Devuelve el último mensaje o None si no existe.
    """
    if historial:
        return historial[-1]
    return None


def contar_mensajes(historial):
    """
    Devuelve cuántos mensajes hay en el chat.
    """
    return len(historial)
