# -*- coding: utf-8 -*-
"""
Geração de código de três endereços (TAC) a partir da AST já verificada.

Formato das instruções:
    x = y op z          operação binária (op em + - * /)
    x = - y             menos unário
    x = y               cópia
    x = (float) y       conversão int -> float (alargamento implícito)
    ifFalse a rel b goto L
    if a == b goto L    (usado na seleção múltipla)
    goto L
    L:                  rótulo
    print x
    print "texto"

Temporários se chamam t1, t2, ...; um nome já usado por variável do programa
é pulado (senão `radio t1;` seria sobrescrita por um temporário).
Cada instrução guarda a linha do fonte que a gerou, para o interpretador
(interpretador.py) poder relatar erros de execução com a linha.
"""

from . import ast_nodes as A


def nomes_declarados(no, nomes=None):
    """Conjunto com o nome de todas as variáveis declaradas na AST."""
    if nomes is None:
        nomes = set()
    if isinstance(no, A.DeclItem):
        nomes.add(no.nome)
    if isinstance(no, list):
        for x in no:
            nomes_declarados(x, nomes)
    elif isinstance(no, A.No):
        for v in vars(no).values():
            nomes_declarados(v, nomes)
    return nomes


class GeradorTAC:
    def __init__(self):
        self.codigo = []
        self.linhas = []          # linha do fonte de cada instrução de `codigo`
        self.linha = 0            # linha do comando sendo traduzido
        self.n_temp = 0
        self.n_rot = 0
        self.alvos_pare = []      # pilha de rótulos de saída (break)
        self.nomes_programa = set()

    # ---------------- utilitários ----------------
    def temp(self):
        while True:
            self.n_temp += 1
            nome = f"t{self.n_temp}"
            if nome not in self.nomes_programa:
                return nome

    def rotulo(self):
        self.n_rot += 1
        return f"L{self.n_rot}"

    def emit(self, instr):
        self.codigo.append("    " + instr)
        self.linhas.append(self.linha)

    def emit_rotulo(self, r):
        self.codigo.append(f"{r}:")
        self.linhas.append(self.linha)

    def gerar(self, programa):
        self.nomes_programa = nomes_declarados(programa)
        for c in programa.comandos:
            self.cmd(c)
        return self.codigo

    # ---------------- expressões ----------------
    def expr(self, no):
        """Gera código para a expressão e devolve o endereço do resultado."""
        if isinstance(no, A.Num):
            return str(no.valor)
        if isinstance(no, A.Var):
            return no.nome
        if isinstance(no, A.Negativo):
            a = self.expr(no.expr)
            t = self.temp()
            self.emit(f"{t} = - {a}")
            return t
        if isinstance(no, A.BinOp):
            a = self.para_tipo(no.esq, no.tipo)
            b = self.para_tipo(no.dir, no.tipo)
            t = self.temp()
            self.emit(f"{t} = {a} {no.op} {b}")
            return t
        raise TypeError(no)

    def para_tipo(self, no, tipo_destino):
        """Gera a expressão e converte int -> float se necessário."""
        end = self.expr(no)
        if tipo_destino == "float" and getattr(no, "tipo", None) == "int":
            if isinstance(no, A.Num):
                return f"{float(no.valor)}"
            t = self.temp()
            self.emit(f"{t} = (float) {end}")
            return t
        return end

    def condicao_falsa(self, cond, destino):
        anterior, self.linha = self.linha, cond.linha
        tipo = "float" if "float" in (cond.esq.tipo, cond.dir.tipo) else "int"
        a = self.para_tipo(cond.esq, tipo)
        b = self.para_tipo(cond.dir, tipo)
        self.emit(f"ifFalse {a} {cond.op} {b} goto {destino}")
        self.linha = anterior

    # ---------------- comandos ----------------
    def cmd(self, no):
        anterior, self.linha = self.linha, no.linha
        getattr(self, "cmd_" + type(no).__name__)(no)
        self.linha = anterior

    def bloco(self, b):
        for c in b.comandos:
            self.cmd(c)

    def cmd_Declaracao(self, no):
        for it in no.itens:
            if it.init is not None:
                self.linha = it.linha
                self.emit(f"{it.nome} = {self.para_tipo(it.init, no.tipo)}")

    def cmd_Atribuicao(self, no):
        self.emit(f"{no.nome} = {self.para_tipo(no.expr, no.tipo)}")

    def cmd_Se(self, no):
        if not no.senaoses and no.senao is None:     # se simples
            fim = self.rotulo()
            self.condicao_falsa(no.cond, fim)
            self.bloco(no.entao)
            self.emit_rotulo(fim)
            return
        fim = self.rotulo()
        prox = self.rotulo()
        self.condicao_falsa(no.cond, prox)
        self.bloco(no.entao)
        self.emit(f"goto {fim}")
        self.emit_rotulo(prox)
        for s in no.senaoses:
            prox = self.rotulo()
            self.condicao_falsa(s.cond, prox)
            self.bloco(s.bloco)
            self.emit(f"goto {fim}")
            self.emit_rotulo(prox)
        if no.senao is not None:
            self.bloco(no.senao)
        self.emit_rotulo(fim)

    def cmd_Enquanto(self, no):
        inicio, fim = self.rotulo(), self.rotulo()
        self.emit_rotulo(inicio)
        self.condicao_falsa(no.cond, fim)
        self.alvos_pare.append(fim)
        self.bloco(no.corpo)
        self.alvos_pare.pop()
        self.emit(f"goto {inicio}")
        self.emit_rotulo(fim)

    def cmd_Escolha(self, no):
        t = self.expr(no.expr)
        fim = self.rotulo()
        rot_casos = [self.rotulo() for _ in no.casos]
        rot_padrao = self.rotulo() if no.padrao else fim
        # despacho
        for caso, r in zip(no.casos, rot_casos):
            for valor in caso.rotulos:
                self.emit(f"if {t} == {valor} goto {r}")
        self.emit(f"goto {rot_padrao}")
        # corpos (sem 'pare' o fluxo cai no próximo caso, como em C)
        self.alvos_pare.append(fim)
        for caso, r in zip(no.casos, rot_casos):
            self.emit_rotulo(r)
            for c in caso.comandos:
                self.cmd(c)
        if no.padrao:
            self.emit_rotulo(rot_padrao)
            for c in no.padrao.comandos:
                self.cmd(c)
        self.alvos_pare.pop()
        self.emit_rotulo(fim)

    def cmd_Pare(self, no):
        self.emit(f"goto {self.alvos_pare[-1]}")

    def cmd_Imprime(self, no):
        if isinstance(no.expr, A.Texto):
            self.emit(f'print "{no.expr.valor}"')
        else:
            self.emit(f"print {self.expr(no.expr)}")


def gerar_tac(programa):
    return GeradorTAC().gerar(programa)


def gerar_tac_com_linhas(programa):
    """Como gerar_tac, mas devolve pares (instrução, linha do fonte)."""
    g = GeradorTAC()
    g.gerar(programa)
    return list(zip(g.codigo, g.linhas))
