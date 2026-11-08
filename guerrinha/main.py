# -*- coding: utf-8 -*-
"""
Ponto de entrada do compilador.

Uso:
    python main.py programa.grr            # AST + código de três endereços
    python main.py programa.grr --so-ast   # só a AST
    python main.py programa.grr --so-tac   # só o TAC
    python main.py programa.grr --debug    # grava build/parser.out (tabela LALR)
    python main.py --tokens programa.grr   # lista os tokens reconhecidos
    python main.py --palavras              # tabela de palavras reservadas
"""

import argparse
import os
import sys

from guerrinha import frases
from guerrinha.parser import analisar
from guerrinha.lexer import criar_lexer
from guerrinha.semantica import verificar
from guerrinha.tac import gerar_tac
from guerrinha.ast_nodes import imprimir_ast


def compilar(codigo, mostrar_ast=True, mostrar_tac=True, debug=False):
    """Roda as fases em sequência. Devolve True se o programa foi aceito."""
    outdir = None
    if debug:
        outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        os.makedirs(outdir, exist_ok=True)

    # Fase 1: léxico + sintático (o parser puxa tokens do lexer)
    ast, erros = analisar(codigo, debug=debug, outputdir=outdir)
    if erros:
        for e in erros:
            print(e)
        return False

    # Fase 2: semântica
    erros = verificar(ast)
    if erros:
        for e in erros:
            print(e)
        return False

    # Fase 3: tradução
    if mostrar_ast:
        print("--- AST ---")
        print(imprimir_ast(ast))
    if mostrar_tac:
        print("--- Código de três endereços ---")
        print("\n".join(gerar_tac(ast)))
    print(f'  >> "{frases.PIADA_SUCESSO}"')
    print(f"  [{frases.NOME_LINGUAGEM}] Programa aceito.")
    return True


def listar_tokens(codigo):
    lexer = criar_lexer()
    lexer.input(codigo)
    for tok in lexer:
        print(f"linha {tok.lineno:>3}  {tok.type:<15} {tok.value!r}")
    for e in lexer.erros:
        print(e)


def tabela_palavras():
    print("| Token | Construção | Frase |")
    print("|---|---|---|")
    papeis = {
        "TIPO_INT": "tipo inteiro", "TIPO_FLOAT": "tipo fracionário",
        "SE": "if", "SENAOSE": "else if", "SENAO": "else",
        "ESCOLHA": "switch", "CASO": "case", "PARE": "break",
        "PADRAO": "default", "ENQUANTO": "while", "IMPRIME": "print",
    }
    for tok, f in frases.PALAVRAS_RESERVADAS.items():
        print(f"| {tok} | {papeis.get(tok, '')} | `{f}` |")


def main():
    ap = argparse.ArgumentParser(description=f"Compilador {frases.NOME_LINGUAGEM}")
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--so-ast", action="store_true")
    ap.add_argument("--so-tac", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--tokens", action="store_true")
    ap.add_argument("--palavras", action="store_true")
    args = ap.parse_args()

    if args.palavras:
        tabela_palavras()
        return 0
    if not args.arquivo:
        ap.error("informe o arquivo-fonte")

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    if args.tokens:
        listar_tokens(codigo)
        return 0

    print(f"=== {frases.NOME_LINGUAGEM} · {os.path.basename(args.arquivo)} ===")
    ok = compilar(codigo,
                  mostrar_ast=not args.so_tac,
                  mostrar_tac=not args.so_ast,
                  debug=args.debug)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
