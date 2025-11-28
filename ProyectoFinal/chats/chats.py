# chats/chats.py

def crear_mensaje(role, content):

    return {
        "role": role,
        "content": content
    }


def agregar_mensaje(historial, role, content):
    
    #Agrega un mensaje al historial (lista).
    #Devuelve el historial actualizado.
    historial.append(crear_mensaje(role, content))
    return historial


def limpiar_chat():
    return []


def borrar_ultimo_mensaje(historial):
    if historial:
        historial.pop()
    return historial


def obtener_ultimo_mensaje(historial):
    if historial:
        return historial[-1]
    return None


def contar_mensajes(historial):
    return len(historial)
