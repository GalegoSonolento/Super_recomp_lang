# -*- coding: utf-8 -*-
"""
Experimento para o relatório (seção 3, Decisões de projeto):
gera a tabela LALR COM e SEM a tabela de precedência dos operadores
aritméticos e mostra quantos conflitos shift/reduce aparecem.

Uso (na raiz do projeto):  python ferramentas/experimento_conflitos.py
Gera build/com_precedencia.out e build/sem_precedencia.out.
"""

import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import inspect  # noqa: E402
import ply.yacc as yacc  # noqa: E402
import guerrinha.parser as P  # noqa: E402

BUILD = os.path.join(RAIZ, "build")
os.makedirs(BUILD, exist_ok=True)


def gerar(nome_arquivo):
    kw = dict(module=P, debug=True, debugfile=nome_arquivo, outputdir=BUILD)
    if "write_tables" in inspect.signature(yacc.yacc).parameters:
        kw["write_tables"] = False
    yacc.yacc(**kw)
    with open(os.path.join(BUILD, nome_arquivo), encoding="utf-8") as f:
        txt = f.read()
    sr = len(re.findall(r"shift/reduce conflict for \S+ in state", txt))
    rr = len(re.findall(r"reduce/reduce conflict in state", txt))
    return sr, rr


original = P.precedence
print("COM precedência:", "S/R=%d R/R=%d" % gerar("com_precedencia.out"))
P.precedence = (("right", "MENOS_UNARIO"),)    # remove só os binários
print("SEM precedência:", "S/R=%d R/R=%d" % gerar("sem_precedencia.out"))
P.precedence = original
print("Detalhes (estados e tokens de cada conflito) em build/*.out")
