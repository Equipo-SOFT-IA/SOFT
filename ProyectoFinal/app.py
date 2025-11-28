import streamlit as st
import os
from dotenv import load_dotenv

#  IMPORTAR MÓDULOS MODULARES
from estilos import configurar_estilos

# AUTH
from auth.usuarios import (
    crear_usuario, verificar_usuario, validar_usuario, validar_contrasena,
    obtener_chats_usuario, cargar_mensajes_chat, guardar_mensajes_chat,
    cargar_archivos_usuario, guardar_archivo_usuario
)

# CHATS (lógica interna)
from chats.chats import (
    crear_mensaje, agregar_mensaje
)

# ARCHIVOS
from archivos.pdf import procesar_pdf
from archivos.docx import procesar_docx
from archivos.imagen import cargar_imagen
from archivos.ocr import extraer_texto_ocr

# BIBLIOGRAFÍA
from bibliografia.resumenes import (
    guardar_en_bibliografia, cargar_resumenes
)
from bibliografia.fragmentos import buscar_fragmentos

# IA
from ia.prompt import construir_prompt
from ia.deepseek import enviar_a_deepseek


#  CONFIGURACIÓN INICIAL
st.set_page_config(page_title="SOFT-IA", layout="wide")
load_dotenv()
configurar_estilos()

# Estado inicial
if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = "Chat principal"

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "resumenes" not in st.session_state:
    st.session_state.resumenes = cargar_resumenes()


# -----------------------------------------
#  LOGIN Y REGISTRO
# -----------------------------------------
if not st.session_state.logueado:

    st.title("SOFT-IA — Agente de Ingeniería de Software")
    modo = st.radio("Modo de uso:", ["Invitado", "Registrarse / Iniciar sesión"])

    # INVITADO
    if modo == "Invitado":
        if st.button("Usar como invitado"):
            st.session_state.logueado = True
            st.session_state.usuario = None
            st.session_state.mensajes = []
            st.rerun()

    # REGISTRO & LOGIN
    else:
        # REGISTRO
        with st.form("registro"):
            st.subheader("Crear cuenta")
            nuevo = st.text_input("Usuario", key="reg_user")
            contrasena = st.text_input("Contraseña", type="password", key="reg_pass")
            repetir = st.text_input("Repetir contraseña", type="password", key="reg_pass2")

            if st.form_submit_button("Crear cuenta"):
                error_user = validar_usuario(nuevo)
                error_pass = validar_contrasena(contrasena)

                if error_user:
                    st.error(error_user)
                elif error_pass:
                    st.error(error_pass)
                elif contrasena != repetir:
                    st.error("Las contraseñas no coinciden.")
                elif not crear_usuario(nuevo, contrasena):
                    st.error("El usuario ya existe.")
                else:
                    st.success(f"¡Bienvenido {nuevo}! Cuenta creada.")
                    st.session_state.logueado = True
                    st.session_state.usuario = nuevo
                    st.session_state.chat_actual = "Chat principal"
                    st.session_state.mensajes = []
                    st.rerun()

        # LOGIN
        with st.form("login"):
            st.subheader("Iniciar sesión")
            nombre = st.text_input("Usuario", key="login_user")
            passw = st.text_input("Contraseña", type="password", key="login_pass")

            if st.form_submit_button("Entrar"):
                if not nombre or not passw:
                    st.warning("Completa todos los campos.")
                elif not verificar_usuario(nombre, passw):
                    st.error("Usuario o contraseña incorrectos.")
                else:
                    st.session_state.logueado = True
                    st.session_state.usuario = nombre
                    st.session_state.chat_actual = "Chat principal"
                    st.session_state.mensajes = cargar_mensajes_chat(nombre, "Chat principal")
                    st.success(f"Hola de nuevo, {nombre}.")
                    st.rerun()


# -----------------------------------------
#  INTERFAZ PRINCIPAL
# -----------------------------------------
if st.session_state.logueado:

    st.sidebar.write(f"👤 Usuario: {st.session_state.usuario or 'Invitado'}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.session_state.usuario = None
        st.session_state.mensajes = []
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💬 Historial de Chats")

    # Selección de chats
    if st.session_state.usuario:
        chats_user = obtener_chats_usuario(st.session_state.usuario)

        chat_seleccionado = st.sidebar.selectbox(
            "Seleccionar chat:",
            chats_user,
            index=chats_user.index(st.session_state.chat_actual)
        )

        if chat_seleccionado != st.session_state.chat_actual:
            st.session_state.chat_actual = chat_seleccionado
            st.session_state.mensajes = cargar_mensajes_chat(
                st.session_state.usuario, chat_seleccionado
            )
            st.rerun()

        nuevo_chat = st.sidebar.text_input("🆕 Nombre del nuevo chat")
        if st.sidebar.button("Crear chat"):
            if nuevo_chat and nuevo_chat not in chats_user:
                guardar_mensajes_chat(st.session_state.usuario, nuevo_chat, [])
                st.session_state.chat_actual = nuevo_chat
                st.session_state.mensajes = []
                st.sidebar.success(f"Chat '{nuevo_chat}' creado.")
                st.rerun()

    else:
        st.sidebar.info("Modo invitado: tus chats no se guardarán.")


    #---Subir archivos a bibliografía-------------------------------------------
    archivo_biblio = st.sidebar.file_uploader(
        "Subir archivo a Bibliografía",
        type=["pdf", "docx"]
    )

    if archivo_biblio:
        nombre = archivo_biblio.name.split(".")[0]
        extension = archivo_biblio.name.lower()

        if extension.endswith(".pdf"):
            texto = procesar_pdf(archivo_biblio)
        else:
            texto = procesar_docx(archivo_biblio)

        guardar_en_bibliografia(nombre, texto)
        st.sidebar.success(f"'{nombre}' agregado a la bibliografía.")


    # -----------------------------------------
    #  CHAT PRINCIPAL
    # -----------------------------------------
    st.title("🤖 SOFT-IA")
    st.markdown("<h3 style='text-align: center; color: #8B949E;'>Agente Especializado en Ingeniería de Software</h3>", unsafe_allow_html=True)
    st.markdown("---")

    chat_area = st.container()

    # Mostrar historial
    with chat_area:
        for msg in st.session_state.mensajes:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Subir archivo al chat
    archivo = st.file_uploader("Subir archivo", type=["pdf", "docx", "png", "jpg", "jpeg"])

    if archivo:
        nombre = archivo.name.lower()

        if nombre.endswith(".pdf"):
            contenido = {"tipo": "texto", "texto": procesar_pdf(archivo)}

        elif nombre.endswith(".docx"):
            contenido = {"tipo": "texto", "texto": procesar_docx(archivo)}

        else:
            if nombre.endswith((".png",".jpg",".jpeg")):
                img_info = cargar_imagen(archivo)
                if img_info["tipo"] == "imagen":
                    contenido = extraer_texto_ocr(img_info["imagen"])
                else:
                    contenido = img_info
            else:
                st.error("Tipo de archivo no permitido")
        if st.session_state.usuario:
            guardar_archivo_usuario(st.session_state.usuario, archivo.name, contenido)
            st.toast(f"Archivo '{archivo.name}' guardado.", icon="💾")


    # -----------------------------------------
    #  INPUT DEL CHAT
    # -----------------------------------------
    if mensaje_usuario := st.chat_input(f"[{st.session_state.chat_actual}] ¿En qué puedo ayudarte?"):

        # Guardar mensaje del usuario
        agregar_mensaje(st.session_state.mensajes, "user", mensaje_usuario)

        with chat_area.chat_message("user", avatar="🧑‍💻"):
            st.markdown(mensaje_usuario)

        # Preparar memoria basada en archivos subidos
        memoria_archivos = []
        if st.session_state.usuario:
            for a in cargar_archivos_usuario(st.session_state.usuario):
                if a["contenido"]["tipo"] == "texto":
                    memoria_archivos.append(
                        f"[Archivo: {a['nombre']}]\n{a['contenido']['texto'][:30000]}"
                    )

        memoria_str = "\n\n".join(memoria_archivos)

        # Buscar fragmentos relevantes
        resumenes = cargar_resumenes()
        fragmentos = buscar_fragmentos(mensaje_usuario, resumenes)

        # Construir prompt con reglas
        prompt = construir_prompt(memoria_str, fragmentos, mensaje_usuario)

        # Ensamblar historial CORRECTO
        mensajes_api = [{"role": "system", "content": prompt}]

        for msg in st.session_state.mensajes:
            if msg["role"] in ["user", "assistant"]:
                mensajes_api.append(msg)

        # Mostrar "pensando..."
        with chat_area.chat_message("assistant", avatar="🤖"):
            st.write("Analizando información...")

        # Llamada a la IA
        respuesta = enviar_a_deepseek(mensajes_api)

        texto_respuesta = respuesta["texto"]

        # Mostrar respuesta
        with chat_area.chat_message("assistant", avatar="🤖"):
            st.markdown(texto_respuesta)

        # Guardar en historial
        agregar_mensaje(st.session_state.mensajes, "assistant", texto_respuesta)

        if st.session_state.usuario:
            guardar_mensajes_chat(
                st.session_state.usuario,
                st.session_state.chat_actual,
                st.session_state.mensajes
            )
