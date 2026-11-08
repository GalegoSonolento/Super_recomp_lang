# -*- coding: utf-8 -*-
"""
Gera colab/Guerrinha.ipynb: um notebook AUTOSSUFICIENTE para o Google Colab.

Cada arquivo do projeto vira uma célula %%writefile, então basta subir o .ipynb
no Colab e executar "Ambiente de execução > Executar tudo" (sem ajustes, como
pede o enunciado). Rode este script de novo sempre que mudar o código.

Uso (na raiz do projeto):  python ferramentas/gerar_notebook.py
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from guerrinha import frases  # noqa: E402

SAIDA = os.path.join(RAIZ, "colab", f"{frases.NOME_LINGUAGEM}.ipynb")

ORDEM_FONTES = [
    "guerrinha/__init__.py",
    "guerrinha/erros.py",
    "guerrinha/lexer.py",
    "guerrinha/ast_nodes.py",
    "guerrinha/parser.py",
    "guerrinha/semantica.py",
    "guerrinha/tac.py",
    "main.py",
    "ferramentas/rodar_testes.py",
    "ferramentas/experimento_conflitos.py",
]


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


def md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto}


def code(texto):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": texto}


def writefile(rel):
    return code(f"%%writefile {rel}\n{ler(rel)}")


def testes():
    out = []
    for pasta in ("validos", "invalidos"):
        d = os.path.join(RAIZ, "testes", pasta)
        out += [f"testes/{pasta}/{n}" for n in sorted(os.listdir(d))]
    return out


def main():
    nome = frases.NOME_LINGUAGEM
    lista_testes = testes()
    pastas = ["guerrinha", "ferramentas", "testes/validos", "testes/invalidos"]
    cells = [
        md(f"# {nome} — Trabalho do Grau B (Compiladores)\n\n"
           "Notebook gerado por `ferramentas/gerar_notebook.py`. "
           "Execute **Ambiente de execução → Executar tudo**.\n\n"
           "Seções: 1) instalação · 2) frases da linguagem · 3) código do "
           "compilador · 4) programas de teste · 5) execução · 6) teste livre."),
        md("## 1. Instalação"),
        code("!pip -q install ply\nimport os\n"
             f"for d in {pastas!r}:\n    os.makedirs(d, exist_ok=True)"),
        md("## 2. Frases da linguagem (palavras reservadas e mensagens)\n"
           "Único lugar onde se trocam as palavras."),
        writefile("guerrinha/frases.py"),
        md("## 3. Código do compilador"),
        *[writefile(r) for r in ORDEM_FONTES],
        md("## 4. Programas de teste"),
        *[writefile(r) for r in lista_testes],
        md("## 5. Execução\n### 5.1 Todos os testes"),
        code("!python ferramentas/rodar_testes.py"),
        md("### 5.2 Conflitos da gramática (com e sem precedência)"),
        code("!python ferramentas/experimento_conflitos.py"),
        md("### 5.3 Programas válidos (AST + código de três endereços)"),
        *[code(f"!python main.py {r}") for r in lista_testes if "/validos/" in r],
        md("### 5.4 Programas inválidos (mensagem + linha)"),
        *[code(f"!python main.py {r}") for r in lista_testes if "/invalidos/" in r],
        md(f"## 6. Teste livre\nEdite o programa abaixo e execute as duas células."),
        code(f"%%writefile meu_programa{frases.EXTENSAO}\n"
             f"{frases.PALAVRAS_RESERVADAS['TIPO_INT']} x = 1;\n"
             f"{frases.PALAVRAS_RESERVADAS['IMPRIME']} (x + 1);\n"),
        code(f"!python main.py meu_programa{frases.EXTENSAO}"),
    ]
    nb = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}, "colab": {"provenance": []}},
        "nbformat": 4, "nbformat_minor": 0}
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Notebook gerado: {os.path.relpath(SAIDA, RAIZ)} ({len(cells)} células)")


if __name__ == "__main__":
    main()
