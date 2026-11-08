# Contexto para o Claude Code

Trabalho de Compiladores (Unisinos, TGB). Enunciado: `docs/referencia/`.
Python 3 + PLY 3.11 (`pip install ply`). Precisa rodar no Google Colab sem ajustes.

- Palavras reservadas e mensagens ficam SÓ em `guerrinha/frases.py`. As chaves (nomes de token) não mudam.
- Depois de mudar código ou testes: `python ferramentas/rodar_testes.py` (precisa dar 0 falhas) e `python ferramentas/gerar_notebook.py`.
- A gramática tem 0 conflitos. Conferir com `python ferramentas/experimento_conflitos.py` e manter `docs/gramatica.md` em sincronia com as docstrings de `parser.py`.
- Toda mensagem de erro precisa ter o número da linha (`erros.Erro`).
- Decisões novas vão para `docs/decisoes.md` no formato benefício / por quê / contraponto.
- Responder em português, de forma breve.
