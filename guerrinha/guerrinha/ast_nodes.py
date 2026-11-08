# -*- coding: utf-8 -*-
"""
Nós da árvore sintática abstrata (AST).

A AST é construída nas AÇÕES SEMÂNTICAS do parser (tradução dirigida por
sintaxe). Cada nó guarda a linha de origem para as mensagens de erro.
`tipo` é preenchido depois, pela verificação semântica.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class No:
    linha: int


# ---------------- Expressões ----------------
@dataclass
class Num(No):
    valor: object                 # int ou float
    tipo: Optional[str] = None


@dataclass
class Var(No):
    nome: str
    tipo: Optional[str] = None


@dataclass
class BinOp(No):
    op: str                       # + - * /
    esq: No
    dir: No
    tipo: Optional[str] = None


@dataclass
class Negativo(No):               # menos unário
    expr: No
    tipo: Optional[str] = None


@dataclass
class Condicao(No):
    op: str                       # == != > < >= <=
    esq: No
    dir: No


# ---------------- Comandos ----------------
@dataclass
class DeclItem(No):
    nome: str
    init: Optional[No] = None


@dataclass
class Declaracao(No):
    tipo: str                     # "int" | "float"
    itens: List[DeclItem]


@dataclass
class Atribuicao(No):
    nome: str
    expr: No
    tipo: Optional[str] = None    # tipo da variável-alvo (preenchido na semântica)


@dataclass
class Bloco(No):
    comandos: List[No]


@dataclass
class Se(No):
    cond: Condicao
    entao: Bloco
    senaoses: List["SenaoSe"] = field(default_factory=list)
    senao: Optional[Bloco] = None


@dataclass
class SenaoSe(No):
    cond: Condicao
    bloco: Bloco


@dataclass
class Enquanto(No):
    cond: Condicao
    corpo: Bloco


@dataclass
class Caso(No):
    rotulos: List[int]            # vazio = caso padrão
    comandos: List[No]


@dataclass
class Escolha(No):
    expr: No
    casos: List[Caso]
    padrao: Optional[Caso] = None


@dataclass
class Pare(No):
    pass


@dataclass
class Imprime(No):
    expr: No


@dataclass
class Programa(No):
    comandos: List[No]


# ---------------- Impressão da AST ----------------
def imprimir_ast(no, nivel=0):
    """Devolve a AST como texto indentado."""
    pad = "  " * nivel
    linhas = []

    def filho(rotulo, n):
        linhas.append(f"{pad}  {rotulo}:")
        linhas.append(imprimir_ast(n, nivel + 2))

    if isinstance(no, Programa):
        linhas.append(f"{pad}Programa")
        for c in no.comandos:
            linhas.append(imprimir_ast(c, nivel + 1))
    elif isinstance(no, Declaracao):
        linhas.append(f"{pad}Declaração {no.tipo}  (linha {no.linha})")
        for it in no.itens:
            linhas.append(f"{pad}  {it.nome}")
            if it.init is not None:
                linhas.append(imprimir_ast(it.init, nivel + 2))
    elif isinstance(no, Atribuicao):
        linhas.append(f"{pad}Atribuição {no.nome} =  (linha {no.linha})")
        linhas.append(imprimir_ast(no.expr, nivel + 1))
    elif isinstance(no, Bloco):
        for c in no.comandos:
            linhas.append(imprimir_ast(c, nivel))
    elif isinstance(no, Se):
        linhas.append(f"{pad}Se  (linha {no.linha})")
        filho("condição", no.cond)
        filho("então", no.entao)
        for s in no.senaoses:
            filho(f"senão-se (linha {s.linha}) condição", s.cond)
            filho("bloco", s.bloco)
        if no.senao is not None:
            filho("senão", no.senao)
    elif isinstance(no, Enquanto):
        linhas.append(f"{pad}Enquanto  (linha {no.linha})")
        filho("condição", no.cond)
        filho("corpo", no.corpo)
    elif isinstance(no, Escolha):
        linhas.append(f"{pad}Escolha  (linha {no.linha})")
        filho("expressão", no.expr)
        for c in no.casos + ([no.padrao] if no.padrao else []):
            rot = ", ".join(map(str, c.rotulos)) if c.rotulos else "padrão"
            linhas.append(f"{pad}  caso {rot}:")
            for cmd in c.comandos:
                linhas.append(imprimir_ast(cmd, nivel + 2))
    elif isinstance(no, Pare):
        linhas.append(f"{pad}Pare  (linha {no.linha})")
    elif isinstance(no, Imprime):
        linhas.append(f"{pad}Imprime  (linha {no.linha})")
        linhas.append(imprimir_ast(no.expr, nivel + 1))
    elif isinstance(no, Condicao):
        linhas.append(f"{pad}{no.op}")
        linhas.append(imprimir_ast(no.esq, nivel + 1))
        linhas.append(imprimir_ast(no.dir, nivel + 1))
    elif isinstance(no, BinOp):
        sufixo = f"  : {no.tipo}" if no.tipo else ""
        linhas.append(f"{pad}{no.op}{sufixo}")
        linhas.append(imprimir_ast(no.esq, nivel + 1))
        linhas.append(imprimir_ast(no.dir, nivel + 1))
    elif isinstance(no, Negativo):
        linhas.append(f"{pad}- (unário)")
        linhas.append(imprimir_ast(no.expr, nivel + 1))
    elif isinstance(no, Num):
        linhas.append(f"{pad}{no.valor}")
    elif isinstance(no, Var):
        linhas.append(f"{pad}{no.nome}")
    else:
        linhas.append(f"{pad}?? {type(no).__name__}")
    return "\n".join(l for l in linhas if l != "")
