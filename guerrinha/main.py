# -*- coding: utf-8 -*-
"""
Ponto de entrada: compila e EXECUTA um programa.

Uso:
    python main.py programa.grr            # compila e executa (erros com a linha)
    python main.py programa.grr -gt        # idem + grava programa.txt ao lado do
                                           #   .grr (AST + TAC, ou os erros)
    python main.py programa.grr -c         # só compila: mostra AST + TAC, não executa
    python main.py programa.grr --so-ast   # só compila: mostra só a AST
    python main.py programa.grr --so-tac   # só compila: mostra só o TAC
    python main.py programa.grr --debug    # grava build/parser.out (tabela LALR)
    python main.py --tokens programa.grr   # lista os tokens reconhecidos
    python main.py --palavras              # tabela de palavras reservadas

Código de saída: 0 = ok; 1 = erro (léxico, sintático, semântico ou de execução).
"""

import argparse
import contextlib
import io
import os
import sys

from guerrinha import frases
from guerrinha.parser import analisar
from guerrinha.lexer import criar_lexer
from guerrinha.semantica import verificar
from guerrinha.tac import gerar_tac, gerar_tac_com_linhas
from guerrinha.ast_nodes import imprimir_ast
from guerrinha.interpretador import executar


def analisar_completo(codigo, debug=False):
    """Léxico + sintático + semântico. Devolve (ast, erros)."""
    outdir = None
    if debug:
        outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
        os.makedirs(outdir, exist_ok=True)

    # Fase 1: léxico + sintático (o parser puxa tokens do lexer)
    ast, erros = analisar(codigo, debug=debug, outputdir=outdir)
    if erros:
        return None, erros

    # Fase 2: semântica
    erros = verificar(ast)
    if erros:
        return None, erros
    return ast, []


def compilar(codigo, mostrar_ast=True, mostrar_tac=True, debug=False):
    """Compila e imprime AST/TAC (ou os erros). Devolve True se foi aceito."""
    ast, erros = analisar_completo(codigo, debug)
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


def rodar(codigo, debug=False):
    """Compila e, se não houver erro, executa. Devolve True se tudo deu certo."""
    ast, erros = analisar_completo(codigo, debug)
    if not erros:
        # Fase 4: execução do código de três endereços
        erros = executar(gerar_tac_com_linhas(ast))
    for e in erros:
        print(e)
    return not erros


def gerar_txt(arquivo, codigo, debug=False):
    """Grava, ao lado do fonte, o .txt com AST + TAC (ou os erros)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        compilar(codigo, debug=debug)
    destino = os.path.splitext(arquivo)[0] + ".txt"
    with open(destino, "w", encoding="utf-8") as f:
        f.write(buf.getvalue())
    print(f"[{frases.NOME_LINGUAGEM}] Saída gravada em {destino}", file=sys.stderr)


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
    ap = argparse.ArgumentParser(
        description=f"{frases.NOME_LINGUAGEM}: compila e executa um programa "
                    f"{frases.EXTENSAO}.")
    ap.add_argument("arquivo", nargs="?", help=f"programa-fonte ({frases.EXTENSAO})")
    ap.add_argument("-gt", "--gentxt", action="store_true",
                    help="grava <arquivo>.txt ao lado do fonte com AST + TAC "
                         "(ou os erros)")
    ap.add_argument("-c", "--compilar", action="store_true",
                    help="só compila: mostra AST + TAC no terminal, não executa")
    ap.add_argument("--so-ast", action="store_true",
                    help="só compila: mostra só a AST")
    ap.add_argument("--so-tac", action="store_true",
                    help="só compila: mostra só o TAC")
    ap.add_argument("--debug", action="store_true",
                    help="grava build/parser.out (tabela LALR)")
    ap.add_argument("--tokens", action="store_true",
                    help="lista os tokens reconhecidos")
    ap.add_argument("--palavras", action="store_true",
                    help="tabela de palavras reservadas")
    args = ap.parse_args()

    if args.palavras:
        tabela_palavras()
        return 0
    if not args.arquivo:
        ap.error("informe o arquivo-fonte")

    try:
        with open(args.arquivo, encoding="utf-8") as f:
            codigo = f.read()
    except OSError as e:
        print(f"[{frases.NOME_LINGUAGEM}] Não foi possível abrir "
              f"'{args.arquivo}': {e.strerror}.", file=sys.stderr)
        return 1

    if args.tokens:
        listar_tokens(codigo)
        return 0

    if args.gentxt:
        gerar_txt(args.arquivo, codigo, debug=args.debug)

    if args.compilar or args.so_ast or args.so_tac:
        print(f"=== {frases.NOME_LINGUAGEM} · {os.path.basename(args.arquivo)} ===")
        ok = compilar(codigo,
                      mostrar_ast=not args.so_tac,
                      mostrar_tac=not args.so_ast,
                      debug=args.debug)
        return 0 if ok else 1

    try:
        ok = rodar(codigo, debug=args.debug)
    except KeyboardInterrupt:
        print(f"\n[{frases.NOME_LINGUAGEM}] Execução interrompida (Ctrl+C).",
              file=sys.stderr)
        return 130
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
