import markdown
import webbrowser
from pathlib import Path

# Caminho onde o HTML será salvo
output_path = Path("plano_estudo_mat001.html")

# Texto em Markdown
md_text = """
# Plano de Estudo – MAT001

## Revisão dos Principais Conceitos

### 1. Sistema de Numeração Decimal
- **Conceitos**: Composição e decomposição de números.
- **Importância**: Ajuda nas operações matemáticas e na resolução de problemas.

### 2. Operações Básicas
- Adição, Subtração, Multiplicação e Divisão
- Com exemplos práticos do cotidiano.

### 3. Resolução de Problemas
- Situações cotidianas, incentivo ao raciocínio lógico.

### 4. Unidades de Medida
- Peso (g, kg), Distância (m, km), Volume (L, mL)
- Conversões e aplicações práticas.

## Atividades Práticas

- Decompor números (ex: 345 → 3 centenas, 4 dezenas, 5 unidades)
- Resolver problemas com as 4 operações
- Estimar e converter medidas
- Seguir receitas com medidas de massa e volume

## Considerações Finais

- Revisar diariamente em pequenos blocos
- Usar gráficos e figuras para reforço
"""

# Converter para HTML
html_content = markdown.markdown(md_text, extensions=["fenced_code"])

# Adicionar estrutura HTML básica
full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Plano de Estudo - MAT001</title>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Salvar HTML
output_path.write_text(full_html, encoding="utf-8")

# Abrir no navegador
webbrowser.open_new_tab(f"file://{output_path.resolve()}")