# -*- coding: utf-8 -*-
"""
Troca uma palavra reservada provisória pela frase nova NOS PROGRAMAS DE TESTE.
Só mexe no código (antes de '//'); comentários ficam como estão.
Casa palavra inteira: trocar 'int' não estraga 'print' nem 'inteiro'.

Uso (na raiz do projeto):
    python ferramentas/trocar_palavra.py "switch" "Frase nova do switch"

Depois disso, edite também guerrinha/frases.py (a mesma frase!) e rode:
    python ferramentas/rodar_testes.py
    python ferramentas/gerar_notebook.py
"""

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from guerrinha import frases  # noqa: E402


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    antiga, nova = sys.argv[1], sys.argv[2]
    padrao = re.compile(rf"(?<!\w){re.escape(antiga)}(?!\w)")
    total = 0
    for pasta in ("validos", "invalidos"):
        d = os.path.join(RAIZ, "testes", pasta)
        for nome in sorted(os.listdir(d)):
            if not nome.endswith(frases.EXTENSAO):
                continue
            caminho = os.path.join(d, nome)
            with open(caminho, encoding="utf-8") as f:
                linhas = f.read().split("\n")
            n_arquivo = 0
            for i, linha in enumerate(linhas):
                codigo, sep, comentario = linha.partition("//")
                novo, n = padrao.subn(lambda _m: nova, codigo)
                linhas[i] = novo + sep + comentario
                n_arquivo += n
            if n_arquivo:
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write("\n".join(linhas))
                print(f"{pasta}/{nome}: {n_arquivo} troca(s)")
                total += n_arquivo
    print(f"Total: {total} troca(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
