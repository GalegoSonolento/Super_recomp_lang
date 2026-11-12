# -*- coding: utf-8 -*-
"""
Interpretador do código de três endereços (TAC) gerado por tac.py.

É o que faz um programa "rodar": percorre as instruções com um contador de
programa (pc), guarda os valores das variáveis e dos temporários num
dicionário e desvia nos goto/ifFalse/if. Instruções aceitas (ver tac.py):

    x = y op z    x = - y    x = y    x = (float) y
    ifFalse a rel b goto L    if a == b goto L    goto L    L:
    print x    print "texto"

Tipos em tempo de execução: int do Python para o inteiro da linguagem e float
para o fracionário. Como o TAC já traz as conversões (float) explícitas, basta
olhar o tipo Python dos operandos: int / int trunca em direção a zero (como C).

Erros de execução (com a linha do fonte):
  * divisão por zero;
  * variável lida antes de receber valor (declarada sem valor inicial).
"""

import operator

from .erros import Erro

FASE = "em tempo de execução"
CATEGORIA = "execução"

_RELACIONAIS = {
    "==": operator.eq, "!=": operator.ne,
    ">": operator.gt, "<": operator.lt,
    ">=": operator.ge, "<=": operator.le,
}


class ErroExecucao(Exception):
    def __init__(self, linha, mensagem):
        super().__init__(mensagem)
        self.erro = Erro(FASE, linha, mensagem, categoria=CATEGORIA)


def _dividir(a, b, linha):
    if b == 0:
        raise ErroExecucao(linha, "divisão por zero.")
    if isinstance(a, int) and isinstance(b, int):
        q = abs(a) // abs(b)                  # trunca em direção a zero
        return -q if (a < 0) != (b < 0) else q
    return a / b


_ARITMETICOS = {
    "+": lambda a, b, _l: a + b,
    "-": lambda a, b, _l: a - b,
    "*": lambda a, b, _l: a * b,
    "/": _dividir,
}


class Interpretador:
    def __init__(self, instrucoes, escrever=print):
        """instrucoes: lista de (texto, linha) de tac.gerar_tac_com_linhas."""
        self.codigo = [(t.strip(), linha) for t, linha in instrucoes]
        self.rotulos = {t[:-1]: i for i, (t, _) in enumerate(self.codigo)
                        if t.endswith(":")}
        self.memoria = {}
        self.escrever = escrever

    # ---------------- operandos ----------------
    def valor(self, operando, linha):
        """Literal numérico ou nome de variável/temporário."""
        if operando[0].isdigit() or operando[0] == "-":
            try:
                return int(operando)
            except ValueError:
                return float(operando)
        if operando not in self.memoria:
            raise ErroExecucao(
                linha, f"variável '{operando}' usada antes de receber um "
                       f"valor.")
        return self.memoria[operando]

    # ---------------- execução ----------------
    def executar(self):
        pc = 0
        while pc < len(self.codigo):
            instr, linha = self.codigo[pc]
            pc += 1
            if instr.endswith(":"):
                continue
            destino = self.passo(instr, linha)
            if destino is not None:
                pc = self.rotulos[destino]

    def passo(self, instr, linha):
        """Executa uma instrução. Devolve o rótulo de destino se houver desvio."""
        if instr.startswith('print "'):
            self.escrever(instr[len('print "'):-1])
            return None
        p = instr.split()
        if p[0] == "print":
            self.escrever(str(self.valor(p[1], linha)))
            return None
        if p[0] == "goto":
            return p[1]
        if p[0] in ("ifFalse", "if"):           # if[False] a rel b goto L
            _, a, rel, b, _goto, destino = p
            cond = _RELACIONAIS[rel](self.valor(a, linha), self.valor(b, linha))
            salta = (not cond) if p[0] == "ifFalse" else cond
            return destino if salta else None
        # atribuições: x = ...
        x, _igual, *resto = p
        if len(resto) == 1:                                   # x = y
            v = self.valor(resto[0], linha)
        elif resto[0] == "(float)":                           # x = (float) y
            v = float(self.valor(resto[1], linha))
        elif resto[0] == "-" and len(resto) == 2:             # x = - y
            v = -self.valor(resto[1], linha)
        else:                                                 # x = y op z
            a, op, b = resto
            v = _ARITMETICOS[op](self.valor(a, linha), self.valor(b, linha),
                                 linha)
        self.memoria[x] = v
        return None


def executar(instrucoes, escrever=print):
    """Roda o TAC. Devolve a lista de erros de execução ([] se terminou bem)."""
    try:
        Interpretador(instrucoes, escrever).executar()
    except ErroExecucao as e:
        return [e.erro]
    return []
