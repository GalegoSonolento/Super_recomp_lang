# -*- coding: utf-8 -*-
"""Formatação padronizada das mensagens de erro (sempre com a linha)."""

from . import frases

PIADAS = {
    "léxico": frases.PIADA_ERRO_LEXICO,
    "sintático": frases.PIADA_ERRO_SINTATICO,
    "semântico": frases.PIADA_ERRO_SEMANTICO,
    "tipos": frases.PIADA_ERRO_TIPOS,
}


class Erro:
    """Um erro encontrado em qualquer fase. `categoria` escolhe a piada."""

    def __init__(self, fase, linha, mensagem, categoria=None):
        self.fase = fase                    # "léxico" | "sintático" | "semântico"
        self.linha = linha
        self.mensagem = mensagem
        self.categoria = categoria or fase  # "tipos" usa piada própria

    def __str__(self):
        piada = PIADAS.get(self.categoria, "")
        return (f'  >> "{piada}"\n'
                f"  [{frases.NOME_LINGUAGEM}] Erro {self.fase} na linha "
                f"{self.linha}: {self.mensagem}")
