from openai import OpenAI
import json
from dotenv import load_dotenv
import os

def gerar_json_com_gpt(texto_markdown: str, api_key: str) -> dict:
    client = OpenAI(api_key=api_key)

    prompt = f"""
Você receberá um conteúdo em formato de texto com marcadores. Sua tarefa é:
1. Determinar os níveis hierárquicos dos tópicos, agrupando por título, subtítulo e itens.
2. Sempre retornar uma resposta EM FORMATO EXCLUSIVAMENTE JSON, sem qualquer explicação ou introdução.

Formato esperado:
{{
  "name": "Nome_Disciplina",
  "children": [
    {{
      "name": "Título Principal",
      "children": [
        {{
          "name": "Subtítulo",
          "children": [
            {{ "name": "Item" }}
          ]
        }}
      ]
    }}
  ]
}}

Importante: não adicione comentários, títulos, explicações ou formatação extra. Apenas o JSON puro.

Conteúdo:
{texto_markdown}
    """

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    resposta = response.choices[0].message.content.strip()

    try:
        estrutura = json.loads(resposta)
        if "name" not in estrutura or "children" not in estrutura:
            raise ValueError("JSON recebido não possui a estrutura esperada.")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar a resposta do modelo. JSON inválido:\n" + resposta)

    return estrutura

def salvar_json(estrutura, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(estrutura, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ Variável de ambiente OPENAI_API_KEY não definida.")

    with open("conteudo_programatico.md", "r", encoding="utf-8") as f:
        texto = f.read()

    estrutura = gerar_json_com_gpt(texto_markdown=texto, api_key=api_key)
    salvar_json(estrutura, "dados_arvore.json")

    print("✅ JSON gerado com sucesso: dados_arvore.json")
