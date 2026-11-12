# -*- coding: utf-8 -*-
"""
Analisador léxico (PLY / ply.lex).

As palavras reservadas são FRASES, então não dá para usar o truque clássico
de "reconhece ID e consulta uma tabela". Em vez disso, cada frase de
frases.PALAVRAS_RESERVADAS vira uma expressão regular, e todas são testadas
ANTES do identificador (no PLY, tokens definidos por função são tentados na
ordem em que aparecem no arquivo).
"""

import re
import ply.lex as lex
from ply.lex import TOKEN

from . import frases
from .erros import Erro


# ------------------------------------------------------------------
# Construção das regex das frases
# ------------------------------------------------------------------
def frase_para_regex(frase):
    """'Se algo deu certo, então' -> r'Se\\s+algo\\s+deu\\s+certo\\s*,\\s*então(?!\\w)'"""
    pedacos = re.findall(r"\w+|[^\w\s]", frase)
    regex = ""
    for i, p in enumerate(pedacos):
        if i > 0:
            ambos_palavra = pedacos[i - 1][-1].isalnum() and p[0].isalnum()
            regex += r"\s+" if ambos_palavra else r"\s*"
        regex += re.escape(p)
    if pedacos and pedacos[-1][-1].isalnum():
        regex += r"(?!\w)"           # fronteira de palavra no fim
    return regex


# Frases mais longas primeiro: evita que uma frase que é prefixo de outra
# "roube" o casamento.
_ORDEM = sorted(frases.PALAVRAS_RESERVADAS.items(), key=lambda kv: -len(kv[1]))
_REGEX_FRASE = {tok: re.compile(frase_para_regex(f)) for tok, f in _ORDEM}
REGEX_PALAVRAS = "|".join(f"(?:{frase_para_regex(f)})" for _, f in _ORDEM)


# ------------------------------------------------------------------
# Lista de tokens
# ------------------------------------------------------------------
tokens = tuple(frases.PALAVRAS_RESERVADAS.keys()) + (
    "ID", "NUM_INT", "NUM_FLOAT", "TEXTO",
    "MAIS", "MENOS", "VEZES", "DIVIDE",
    "IGUAL", "DIFERENTE", "MAIOR", "MENOR", "MAIOR_IGUAL", "MENOR_IGUAL",
    "ATRIBUI", "PONTO_VIRGULA", "VIRGULA", "DOIS_PONTOS",
    "ABRE_PAR", "FECHA_PAR", "ABRE_CHAVE", "FECHA_CHAVE",
)

# Símbolos simples (o PLY ordena estas strings da regex mais longa para a
# mais curta, por isso '==' é tentado antes de '=' e '>=' antes de '>').
t_MAIS = r"\+"
t_MENOS = r"-"
t_VEZES = r"\*"
t_DIVIDE = r"/"
t_IGUAL = r"=="
t_DIFERENTE = r"!="
t_MAIOR_IGUAL = r">="
t_MENOR_IGUAL = r"<="
t_MAIOR = r">"
t_MENOR = r"<"
t_ATRIBUI = r"="
t_PONTO_VIRGULA = r";"
t_VIRGULA = r","
t_DOIS_PONTOS = r":"
t_ABRE_PAR = r"\("
t_FECHA_PAR = r"\)"
t_ABRE_CHAVE = r"\{"
t_FECHA_CHAVE = r"\}"

t_ignore = " \t\r"


# ------------------------------------------------------------------
# Tokens definidos por função — A ORDEM IMPORTA
# ------------------------------------------------------------------
def t_COMENTARIO(t):
    r"//[^\n]*"
    pass  # descartado


def t_TEXTO(t):
    r'"[^"\n]*"'
    # Texto entre aspas duplas, numa linha só, sem sequências de escape.
    t.value = t.value[1:-1]
    return t


def t_TEXTO_ABERTO(t):
    r'"[^"\n]*'
    # Aspas abertas que não fecham até o fim da linha.
    t.lexer.erros.append(Erro(
        "léxico", t.lexer.lineno,
        "texto sem aspas de fechamento (o texto precisa abrir e fechar "
        "na mesma linha)."))
    return None


@TOKEN(REGEX_PALAVRAS)
def t_PALAVRA_RESERVADA(t):
    # Descobre QUAL frase casou e troca o tipo do token.
    for tok, rx in _REGEX_FRASE.items():
        if rx.fullmatch(t.value):
            t.type = tok
            break
    t.lexer.lineno += t.value.count("\n")   # frase quebrada em linhas
    return t


def t_NUM_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_NUM_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[^\W\d]\w*"
    # A regex aceita letras acentuadas só para dar UMA mensagem por palavra
    # (ex.: uma frase reservada digitada errado). Identificador válido é ASCII.
    if not t.value.isascii():
        t.lexer.erros.append(Erro(
            "léxico", t.lexer.lineno,
            f"palavra {t.value!r} não reconhecida: identificadores não podem "
            f"ter acento (será que é uma frase reservada digitada errado?)."))
        return None
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.erros.append(Erro(
        "léxico", t.lexer.lineno,
        f"caractere inesperado {t.value[0]!r}."))
    t.lexer.skip(1)


def criar_lexer():
    lexer = lex.lex(reflags=re.UNICODE)
    lexer.erros = []
    return lexer
