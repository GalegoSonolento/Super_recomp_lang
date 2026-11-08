# -*- coding: utf-8 -*-
"""
Verificação semântica (percorre a AST).

Regras implementadas:
  S1. Variável deve ser declarada antes do uso.
  S2. Não pode redeclarar um nome visível (mesmo escopo ou escopo externo).
  S3. Atribuição: int <- float é ERRO; float <- int é permitido (alargamento).
  S4. Expressão do comando de seleção múltipla deve ser int.
  S5. Rótulos de caso não podem se repetir no mesmo comando.
  S6. Encerramento de caso (break) só dentro de seleção múltipla ou laço.

Escopo: cada bloco { } abre um escopo novo (pilha de tabelas de símbolos).
Tipos de expressão: int op int -> int (divisão inteira); qualquer float -> float.
"""

from . import ast_nodes as A
from .erros import Erro


class TabelaSimbolos:
    def __init__(self):
        self.escopos = [{}]

    def abrir(self):
        self.escopos.append({})

    def fechar(self):
        self.escopos.pop()

    def buscar(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None

    def declarar(self, nome, tipo, linha):
        self.escopos[-1][nome] = {"tipo": tipo, "linha": linha}


class Verificador:
    def __init__(self):
        self.ts = TabelaSimbolos()
        self.erros = []
        self.profundidade_pare = 0      # >0 = dentro de escolha/enquanto

    # ---------------- utilitários ----------------
    def erro(self, linha, msg, categoria="semântico"):
        self.erros.append(Erro("semântico", linha, msg, categoria))

    def verificar(self, programa):
        for c in programa.comandos:
            self.cmd(c)
        return self.erros

    # ---------------- comandos ----------------
    def cmd(self, no):
        metodo = getattr(self, "cmd_" + type(no).__name__)
        metodo(no)

    def bloco(self, bloco):
        self.ts.abrir()
        for c in bloco.comandos:
            self.cmd(c)
        self.ts.fechar()

    def cmd_Declaracao(self, no):
        for it in no.itens:
            existente = self.ts.buscar(it.nome)
            if existente:
                self.erro(it.linha,
                          f"variável '{it.nome}' já foi declarada na linha "
                          f"{existente['linha']}.")
                continue
            if it.init is not None:
                t = self.expr(it.init)
                self.checar_atribuicao(it.nome, no.tipo, t, it.linha)
            self.ts.declarar(it.nome, no.tipo, it.linha)

    def cmd_Atribuicao(self, no):
        simbolo = self.ts.buscar(no.nome)
        t_expr = self.expr(no.expr)
        if simbolo is None:
            self.erro(no.linha, f"variável '{no.nome}' não foi declarada.")
            return
        no.tipo = simbolo["tipo"]
        self.checar_atribuicao(no.nome, simbolo["tipo"], t_expr, no.linha)

    def checar_atribuicao(self, nome, t_var, t_expr, linha):
        if t_var == "int" and t_expr == "float":
            self.erro(linha,
                      f"não é possível atribuir valor float à variável "
                      f"int '{nome}'.", categoria="tipos")

    def cmd_Se(self, no):
        self.condicao(no.cond)
        self.bloco(no.entao)
        for s in no.senaoses:
            self.condicao(s.cond)
            self.bloco(s.bloco)
        if no.senao is not None:
            self.bloco(no.senao)

    def cmd_Enquanto(self, no):
        self.condicao(no.cond)
        self.profundidade_pare += 1
        self.bloco(no.corpo)
        self.profundidade_pare -= 1

    def cmd_Escolha(self, no):
        t = self.expr(no.expr)
        if t == "float":
            self.erro(no.linha, "a expressão da seleção múltipla deve ser int, "
                                "mas é float.", categoria="tipos")
        vistos = {}
        self.profundidade_pare += 1
        for caso in no.casos:
            for r in caso.rotulos:
                if r in vistos:
                    self.erro(caso.linha, f"rótulo de caso {r} repetido "
                                          f"(já usado na linha {vistos[r]}).")
                else:
                    vistos[r] = caso.linha
        # Todos os casos compartilham um escopo (como em C): há "fallthrough".
        self.ts.abrir()
        for caso in no.casos + ([no.padrao] if no.padrao else []):
            for c in caso.comandos:
                self.cmd(c)
        self.ts.fechar()
        self.profundidade_pare -= 1

    def cmd_Pare(self, no):
        if self.profundidade_pare == 0:
            self.erro(no.linha, "encerramento de caso fora de seleção "
                                "múltipla ou laço.")

    def cmd_Imprime(self, no):
        self.expr(no.expr)

    # ---------------- expressões ----------------
    def condicao(self, cond):
        self.expr(cond.esq)
        self.expr(cond.dir)

    def expr(self, no):
        """Devolve o tipo ('int' | 'float') ou None se houve erro."""
        if isinstance(no, A.Num):
            return no.tipo
        if isinstance(no, A.Var):
            s = self.ts.buscar(no.nome)
            if s is None:
                self.erro(no.linha, f"variável '{no.nome}' não foi declarada.")
                return None
            no.tipo = s["tipo"]
            return no.tipo
        if isinstance(no, A.Negativo):
            no.tipo = self.expr(no.expr)
            return no.tipo
        if isinstance(no, A.BinOp):
            te, td = self.expr(no.esq), self.expr(no.dir)
            if te is None or td is None:
                return None
            no.tipo = "float" if "float" in (te, td) else "int"
            return no.tipo
        raise TypeError(f"nó de expressão desconhecido: {no}")


def verificar(programa):
    return Verificador().verificar(programa)
