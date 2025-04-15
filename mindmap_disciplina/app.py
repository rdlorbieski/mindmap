import os
import json
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from gerar_json import salvar_json, gerar_json_com_gpt

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Gera JSON caso ainda não exista
if not os.path.exists("dados_arvore.json"):
    with open("conteudo_programatico.md", "r", encoding="utf-8") as f:
        markdown = f.read()
    estrutura = gerar_json_com_gpt(markdown, api_key)
    salvar_json(estrutura, "dados_arvore.json")

# Lê o JSON
with open("dados_arvore.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Lê o HTML e injeta o JSON como string JS
with open("arvore.html", "r", encoding="utf-8") as f:
    html_template = f.read()

html_final = html_template.replace("__JSON_PLACEHOLDER__", json.dumps(json_data))

# Streamlit app
st.set_page_config(layout="wide")
st.title("🌳 Mapa Mental Interativo (Árvore de Conteúdos)")
components.html(html_final, height=3000, scrolling=True)
