# app.py

import os
import json
import streamlit as st
import streamlit.components.v1 as components
from gerar_json import gerar_json_com_gpt
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def verificar_no(no, texto_diarizacao):

    prompt = f"""
    Você é um assistente de análise de aula. 
    Com base no texto abaixo, diga se o seguinte conteúdo foi dado na aula. 
    Responda apenas com "SIM" ou "NÃO".

    Conteúdo: {no['name']}

    Texto da aula:
    {texto_diarizacao}
    """


    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    resposta = response.choices[0].message.content.strip().upper()
    print(resposta)
    if resposta.startswith("SIM"):
        print("Entrou no amarelo")
        no["highlight"] = True
    if "children" in no:
        for filho in no["children"]:
            verificar_no(filho, texto_diarizacao)



def marcar_itens_dados(arvore, texto_diarizacao):
    print(arvore)
    print(texto_diarizacao)
    verificar_no(arvore, texto_diarizacao)
    return arvore

def main():
    st.set_page_config(layout="wide")
    st.title("🌳 Mapa Interativo de Conteúdo Programático com Diarização")

    md_file = st.file_uploader("📄 Envie o conteúdo programático (.md)", type=["md"])
    diarizacao_file = st.file_uploader("🗣️ Envie a transcrição da aula (.txt)", type=["txt"])

    if md_file and diarizacao_file:
        markdown = md_file.read().decode("utf-8")
        diarizacao = diarizacao_file.read().decode("utf-8")

        with st.spinner("🔍 Gerando árvore com GPT..."):
            estrutura = gerar_json_com_gpt(markdown, api_key)

        with st.spinner("🧠 Verificando quais tópicos foram abordados na aula..."):
            estrutura_com_marcas = marcar_itens_dados(estrutura, diarizacao)

        html_template = open("arvore.html", "r", encoding="utf-8").read()
        html_final = html_template.replace("__JSON_PLACEHOLDER__", json.dumps(estrutura_com_marcas))

        st.success("✅ Pronto! Veja abaixo os tópicos abordados (em amarelo):")
        components.html(html_final, height=3000, scrolling=True)

if __name__ == "__main__":
    main()
