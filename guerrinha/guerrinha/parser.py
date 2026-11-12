# -*- coding: utf-8 -*-
"""
Analisador sintático (PLY / ply.yacc, LALR(1)).

Cada função p_* é uma produção: a docstring é a regra BNF e o corpo é a
ação semântica, que constrói o nó da AST (tradução dirigida por sintaxe).
A gramática completa, em BNF, está em docs/gramatica.md.
"""

import inspect
import ply.yacc as yacc

from . import frases
from .erros import Erro
from .lexer import tokens, criar_lexer  # noqa: F401  (o PLY lê `tokens`)
from . import ast_nodes as A


class ErroSintatico(Exception):
    def __init__(self, erro):
        super().__init__(str(erro))
        self.erro = erro


# ------------------------------------------------------------------
# Precedência e associatividade (da MENOR para a MAIOR)
# Resolve os conflitos shift/reduce da gramática ambígua de expressões.
# ------------------------------------------------------------------
precedence = (
    ("left", "MAIS", "MENOS"),
    ("left", "VEZES", "DIVIDE"),
    ("right", "MENOS_UNARIO"),          # token fictício, usado com %prec
)

start = "programa"


# ------------------------------------------------------------------
# Programa e listas de comandos
# ------------------------------------------------------------------
def p_programa(p):
    "programa : lista_cmd"
    p[0] = A.Programa(1, p[1])


def p_lista_cmd(p):
    "lista_cmd : lista_cmd cmd"
    p[0] = p[1] + [p[2]]


def p_lista_cmd_vazia(p):
    "lista_cmd : "
    p[0] = []


def p_cmd(p):
    """cmd : declaracao
           | atribuicao
           | se
           | escolha
           | enquanto
           | imprime
           | pare"""
    p[0] = p[1]


def p_bloco(p):
    "bloco : ABRE_CHAVE lista_cmd FECHA_CHAVE"
    p[0] = A.Bloco(p.lineno(1), p[2])


# ------------------------------------------------------------------
# (a) Declaração de variáveis — individual ou em lista, com init opcional
# ------------------------------------------------------------------
def p_declaracao(p):
    "declaracao : tipo lista_decl PONTO_VIRGULA"
    nome_tipo, linha = p[1]
    p[0] = A.Declaracao(linha, nome_tipo, p[2])


def p_tipo(p):
    """tipo : TIPO_INT
            | TIPO_FLOAT"""
    nome = "int" if p.slice[1].type == "TIPO_INT" else "float"
    p[0] = (nome, p.lineno(1))


def p_lista_decl(p):
    "lista_decl : lista_decl VIRGULA item_decl"
    p[0] = p[1] + [p[3]]


def p_lista_decl_um(p):
    "lista_decl : item_decl"
    p[0] = [p[1]]


def p_item_decl(p):
    "item_decl : ID"
    p[0] = A.DeclItem(p.lineno(1), p[1])


def p_item_decl_init(p):
    "item_decl : ID ATRIBUI expr"
    p[0] = A.DeclItem(p.lineno(1), p[1], p[3])


# ------------------------------------------------------------------
# (e) Atribuição
# ------------------------------------------------------------------
def p_atribuicao(p):
    "atribuicao : ID ATRIBUI expr PONTO_VIRGULA"
    p[0] = A.Atribuicao(p.lineno(1), p[1], p[3])


# ------------------------------------------------------------------
# (b) Condicional: se / senão-se* / senão?
# Blocos com chaves obrigatórias => não há "dangling else".
# ------------------------------------------------------------------
def p_se(p):
    "se : SE ABRE_PAR condicao FECHA_PAR bloco lista_senaose senao_opt"
    p[0] = A.Se(p.lineno(1), p[3], p[5], p[6], p[7])


def p_lista_senaose(p):
    "lista_senaose : lista_senaose SENAOSE ABRE_PAR condicao FECHA_PAR bloco"
    p[0] = p[1] + [A.SenaoSe(p.lineno(2), p[4], p[6])]


def p_lista_senaose_vazia(p):
    "lista_senaose : "
    p[0] = []


def p_senao_opt(p):
    "senao_opt : SENAO bloco"
    p[0] = p[2]


def p_senao_opt_vazio(p):
    "senao_opt : "
    p[0] = None


# ------------------------------------------------------------------
# Laço (extra)
# ------------------------------------------------------------------
def p_enquanto(p):
    "enquanto : ENQUANTO ABRE_PAR condicao FECHA_PAR bloco"
    p[0] = A.Enquanto(p.lineno(1), p[3], p[5])


# ------------------------------------------------------------------
# (c) Seleção múltipla
# ------------------------------------------------------------------
def p_escolha(p):
    "escolha : ESCOLHA ABRE_PAR expr FECHA_PAR ABRE_CHAVE lista_casos padrao_opt FECHA_CHAVE"
    p[0] = A.Escolha(p.lineno(1), p[3], p[6], p[7])


def p_lista_casos(p):
    "lista_casos : lista_casos caso"
    p[0] = p[1] + [p[2]]


def p_lista_casos_um(p):
    "lista_casos : caso"
    p[0] = [p[1]]


def p_caso(p):
    "caso : CASO lista_rotulos DOIS_PONTOS lista_cmd"
    p[0] = A.Caso(p.lineno(1), p[2], p[4])


def p_lista_rotulos(p):
    "lista_rotulos : lista_rotulos VIRGULA rotulo"
    p[0] = p[1] + [p[3]]


def p_lista_rotulos_um(p):
    "lista_rotulos : rotulo"
    p[0] = [p[1]]


def p_rotulo(p):
    "rotulo : NUM_INT"
    p[0] = p[1]


def p_rotulo_negativo(p):
    "rotulo : MENOS NUM_INT"
    p[0] = -p[2]


def p_padrao_opt(p):
    "padrao_opt : PADRAO DOIS_PONTOS lista_cmd"
    p[0] = A.Caso(p.lineno(1), [], p[3])


def p_padrao_opt_vazio(p):
    "padrao_opt : "
    p[0] = None


def p_pare(p):
    "pare : PARE PONTO_VIRGULA"
    p[0] = A.Pare(p.lineno(1))


# ------------------------------------------------------------------
# Saída (extra)
# ------------------------------------------------------------------
def p_imprime(p):
    "imprime : IMPRIME ABRE_PAR expr FECHA_PAR PONTO_VIRGULA"
    p[0] = A.Imprime(p.lineno(1), p[3])


def p_imprime_texto(p):
    "imprime : IMPRIME ABRE_PAR TEXTO FECHA_PAR PONTO_VIRGULA"
    p[0] = A.Imprime(p.lineno(1), A.Texto(p.lineno(3), p[3]))


# ------------------------------------------------------------------
# (f) Condições com os seis operadores relacionais
# ------------------------------------------------------------------
def p_condicao(p):
    """condicao : expr IGUAL expr
                | expr DIFERENTE expr
                | expr MAIOR expr
                | expr MENOR expr
                | expr MAIOR_IGUAL expr
                | expr MENOR_IGUAL expr"""
    p[0] = A.Condicao(p.lineno(2), p[2], p[1], p[3])


# ------------------------------------------------------------------
# (d) Expressões aritméticas
# Gramática ambígua + tabela `precedence` (em vez de expr/termo/fator).
# ------------------------------------------------------------------
def p_expr_binaria(p):
    """expr : expr MAIS expr
            | expr MENOS expr
            | expr VEZES expr
            | expr DIVIDE expr"""
    p[0] = A.BinOp(p.lineno(2), p[2], p[1], p[3])


def p_expr_negativo(p):
    "expr : MENOS expr %prec MENOS_UNARIO"
    p[0] = A.Negativo(p.lineno(1), p[2])


def p_expr_parenteses(p):
    "expr : ABRE_PAR expr FECHA_PAR"
    p[0] = p[2]


def p_expr_int(p):
    "expr : NUM_INT"
    p[0] = A.Num(p.lineno(1), p[1], "int")


def p_expr_float(p):
    "expr : NUM_FLOAT"
    p[0] = A.Num(p.lineno(1), p[1], "float")


def p_expr_id(p):
    "expr : ID"
    p[0] = A.Var(p.lineno(1), p[1])


# ------------------------------------------------------------------
# Erro sintático: para no primeiro erro (sem recuperação).
# ------------------------------------------------------------------
def _descrever(tok):
    if tok.type in frases.PALAVRAS_RESERVADAS:
        return f'palavra reservada "{frases.PALAVRAS_RESERVADAS[tok.type]}"'
    return f"{tok.value!r}"


def p_error(tok):
    if tok is None:
        linha = getattr(_lexer_atual, "ultima_linha", 0)
        msg = "fim de arquivo inesperado (faltou fechar algum bloco ou ';'?)."
    else:
        linha = tok.lineno
        msg = f"token inesperado {_descrever(tok)}."
    raise ErroSintatico(Erro("sintático", linha, msg))


# ------------------------------------------------------------------
# Construção do parser
# ------------------------------------------------------------------
_lexer_atual = None


def criar_parser(debug=False, outputdir=None):
    """debug=True grava parser.out (tabela LALR e conflitos) em outputdir."""
    kwargs = dict(debug=debug)
    if outputdir:
        kwargs["outputdir"] = outputdir
    if "write_tables" in inspect.signature(yacc.yacc).parameters:
        kwargs["write_tables"] = False      # PLY 3.11: não gerar parsetab.py
    return yacc.yacc(**kwargs)


def analisar(codigo, debug=False, outputdir=None):
    """Devolve (ast, erros). Se houver erro léxico ou sintático, ast = None."""
    global _lexer_atual
    # 1ª passada: só o léxico, para relatar TODOS os erros léxicos de uma vez
    # e não gerar erros sintáticos "em cascata" por causa deles.
    lexer = criar_lexer()
    lexer.input(codigo)
    for _ in lexer:
        pass
    if lexer.erros:
        return None, lexer.erros

    # 2ª passada: o parser puxa os tokens do lexer sob demanda.
    lexer = criar_lexer()
    _lexer_atual = lexer
    lexer.ultima_linha = 1
    _token_original = lexer.token

    def token_com_linha():          # lembra a linha do último token lido
        tok = _token_original()
        if tok is not None:
            lexer.ultima_linha = tok.lineno
        return tok
    lexer.token = token_com_linha
    parser = criar_parser(debug, outputdir)
    try:
        ast = parser.parse(codigo, lexer=lexer)
    except ErroSintatico as e:
        return None, [e.erro]
    return ast, []
