import os
import json
import hashlib
import re

# Carpetas donde se guardan los datos
CARPETA_USUARIOS = "usuarios"
os.makedirs(CARPETA_USUARIOS, exist_ok=True)

# ------------------------------------------------------------
# Cifrado de contraseñas
# ------------------------------------------------------------
def cifrar_contrasena(c):
    return hashlib.sha256(c.encode()).hexdigest()


# ------------------------------------------------------------
#  Rutas y Helpers
# ------------------------------------------------------------
def archivo_usuario(nombre_usuario):
    return os.path.join(CARPETA_USUARIOS, f"{nombre_usuario}.json")


def usuario_existe(nombre_usuario):
    return os.path.exists(archivo_usuario(nombre_usuario))


# ------------------------------------------------------------
#  Validación de datos
# ------------------------------------------------------------
def validar_usuario(nombre):
    if not nombre:
        return "El nombre de usuario no puede estar vacío."

    if not re.match(r"^[A-Za-z0-9_ ]+$", nombre):
        return "El nombre de usuario solo puede contener letras, números y guiones bajos."

    if len(nombre) < 3:
        return "El nombre debe tener al menos 3 caracteres."

    return None


def validar_contrasena(passw):
    if not passw:
        return "La contraseña no puede estar vacía."

    if len(passw) < 6:
        return "La contraseña debe tener al menos 6 caracteres."

    if not re.search(r"[A-Za-z]", passw) or not re.search(r"\d", passw):
        return "La contraseña debe contener letras y números."

    return None


# ------------------------------------------------------------
#  Crear y verificar usuario
# ------------------------------------------------------------
def crear_usuario(nombre, contrasena):
    if usuario_existe(nombre):
        return False

    data = {
        "contrasena": cifrar_contrasena(contrasena),
        "chats": {"Chat principal": []},
        "archivos": []
    }

    with open(archivo_usuario(nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True


def verificar_usuario(nombre, contrasena):
    if not usuario_existe(nombre):
        return False

    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["contrasena"] == cifrar_contrasena(contrasena)


# ------------------------------------------------------------
# Manejo de chats
# ------------------------------------------------------------
def obtener_chats_usuario(nombre):
    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.get("chats", {}).keys())


def cargar_mensajes_chat(nombre, chat):
    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("chats", {}).get(chat, [])


def guardar_mensajes_chat(nombre, chat, mensajes):
    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)

    if "chats" not in data:
        data["chats"] = {}

    data["chats"][chat] = mensajes

    with open(archivo_usuario(nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ------------------------------------------------------------
# Manejo de archivos subidos por el usuario
# ------------------------------------------------------------
def cargar_archivos_usuario(nombre):
    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("archivos", [])


def guardar_archivo_usuario(nombre, nombre_archivo, contenido):
    with open(archivo_usuario(nombre), "r", encoding="utf-8") as f:
        data = json.load(f)

    # Evita duplicados
    for a in data["archivos"]:
        if a["nombre"] == nombre_archivo:
            return False

    data["archivos"].append({
        "nombre": nombre_archivo,
        "contenido": contenido
    })

    with open(archivo_usuario(nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True
