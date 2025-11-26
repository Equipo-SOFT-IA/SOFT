import streamlit as st

def configurar_estilos():
    st.markdown("""
        <style>
        /* Tipografía general */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* 1. Título Principal */
        h1 {
            color: #1E88E5 !important;
            text-align: center;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding-bottom: 20px;
            border-bottom: 2px solid #1E88E5;
        }

        /* 2. Burbujas del chat */
        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: rgba(41, 181, 232, 0.1); 
            border-left: 4px solid #29B5E8;
            border-radius: 10px;
            padding: 15px;
        }

        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: rgba(150, 150, 150, 0.1); 
            border-right: 4px solid #1E88E5;
            border-radius: 10px;
            padding: 15px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(41, 181, 232, 0.2);
        }

        /* Botones */
        .stButton > button {
            width: 100%;
            border-radius: 20px;
            border: 1px solid rgba(41, 181, 232, 0.5);
            background-color: transparent; 
            color: inherit;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            border-color: #29B5E8;
            color: white;
            background-color: #1E88E5;
            box-shadow: 0 4px 15px rgba(30, 136, 229, 0.4);
        }

        /* Inputs */
        div[data-baseweb="input"] > div:focus-within {
            border-color: #29B5E8 !important;
            box-shadow: 0 0 0 1px #29B5E8 !important;
        }
        
        div[data-baseweb="input"] > div > input {
            caret-color: #29B5E8;
        }

        /* Radio Buttons */
        div[role="radiogroup"] div[aria-checked="true"] div:first-child {
            background-color: #29B5E8 !important;
            border-color: #29B5E8 !important;
        }

        /* Toast */
        div[data-baseweb="toast"] {
            background-color: #1E88E5 !important;
            color: white !important;
        }

        </style>
    """, unsafe_allow_html=True)
