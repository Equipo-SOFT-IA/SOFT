# ia/deepseek.py

import os
from openai import OpenAI, APIConnectionError

def crear_cliente():
    
    #Crea y devuelve el cliente de DeepSeek usando la API key del entorno.
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )


def enviar_a_deepseek(mensajes_api, modelo="deepseek-chat", temperatura=0.4):
    #Envía los mensajes a DeepSeek y devuelve el texto de la respuesta.
    
    try:
        client = crear_cliente()

        respuesta = client.chat.completions.create(
            model=modelo,
            messages=mensajes_api,
            temperature=temperatura
        )

        return {
            "ok": True,
            "texto": respuesta.choices[0].message.content
        }

    except APIConnectionError:
        return {
            "ok": False,
            "texto": "❌ Error: No se pudo conectar con el servidor de DeepSeek."
        }

    except Exception as e:
        return {
            "ok": False,
            "texto": f"⚠️ Error inesperado al llamar a DeepSeek: {str(e)}"
        }
