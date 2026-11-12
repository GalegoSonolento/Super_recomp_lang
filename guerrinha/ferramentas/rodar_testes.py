# -*- coding: utf-8 -*-
"""
Roda todos os programas de testes/ e grava as saídas em testes/saidas/.

Válidos devem ser ACEITOS; inválidos devem ser REJEITADOS.
Uso (na raiz do projeto):  python ferramentas/rodar_testes.py
"""

import contextlib
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from main import compilar  # noqa: E402
from guerrinha import frases  # noqa: E402

TESTES = os.path.join(RAIZ, "testes")
SAIDAS = os.path.join(TESTES, "saidas")


def main():
    os.makedirs(SAIDAS, exist_ok=True)
    falhas = 0
    for pasta, esperado in (("validos", True), ("invalidos", False)):
        for nome in sorted(os.listdir(os.path.join(TESTES, pasta))):
            if not nome.endswith(frases.EXTENSAO):   # ignora .txt do -gt etc.
                continue
            caminho = os.path.join(TESTES, pasta, nome)
            with open(caminho, encoding="utf-8") as f:
                codigo = f.read()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                aceito = compilar(codigo)
            saida = os.path.join(SAIDAS, os.path.splitext(nome)[0] + ".txt")
            with open(saida, "w", encoding="utf-8") as f:
                f.write(buf.getvalue())
            ok = aceito == esperado
            falhas += not ok
            status = "ok   " if ok else "FALHA"
            resultado = "aceito" if aceito else "rejeitado"
            print(f"[{status}] {pasta}/{nome:<32} -> {resultado}")
    print(f"\n{falhas} falha(s). Saídas em testes/saidas/")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
