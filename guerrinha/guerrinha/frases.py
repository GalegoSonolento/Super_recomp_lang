# -*- coding: utf-8 -*-
"""
=====================================================================
  frases.py  —  ÚNICO ARQUIVO ONDE SE TROCAM PALAVRAS E MENSAGENS
=====================================================================

Tudo que é "texto do Guerrinha" mora aqui. O analisador léxico monta
as expressões regulares das palavras reservadas a partir deste
dicionário, então para trocar uma palavra basta editar a string.

Regras de escrita das frases (decididas no projeto, ver docs/decisoes.md):
  * Diferencia maiúsculas de minúsculas: "Ninguém" != "ninguém".
  * Entre duas palavras da frase, aceita-se QUALQUER quantidade de
    espaço em branco (inclusive quebra de linha).
  * Ao redor de pontuação (vírgula, ?, .) o espaço é opcional.
  * A frase só casa se terminar numa fronteira de palavra
    ("...dólares" não casa com "...dólar").

Marcadores:
  # TODO-FRASE  -> ainda está com a palavra provisória em inglês.
                   Trocar pela frase escolhida e atualizar os testes
                   (buscar/substituir em testes/).
"""

# ---------------------------------------------------------------
# Identidade da linguagem
# ---------------------------------------------------------------
NOME_LINGUAGEM = "Guerrinha"      # TODO-NOME: batizar a linguagem
EXTENSAO = ".grr"                 # extensão dos programas-fonte

# ---------------------------------------------------------------
# Palavras reservadas  (TOKEN -> frase)
# ---------------------------------------------------------------
# A chave (à esquerda) é o nome do token usado na gramática
# (guerrinha/parser.py). NÃO mude as chaves, só as frases.
PALAVRAS_RESERVADAS = {
    # --- tipos (construção a) ---
    "TIPO_INT":   "int",          # TODO-FRASE: tipo inteiro
    "TIPO_FLOAT": "float",        # TODO-FRASE: tipo fracionário

    # --- condicional (construção b) ---
    "SE":         "Ninguém quer saber o preço do dólar",          # if
    "SENAOSE":    "Se algo deu certo, então tem que mudar",       # else if
    "SENAO":      ", nós não temos dólar",                        # else

    # --- seleção múltipla (construção c) ---
    "ESCOLHA":    "switch",       # TODO-FRASE: switch
    "CASO":       "case",         # TODO-FRASE: case
    "PARE":       "break",        # TODO-FRASE: break (encerramento de caso)
    "PADRAO":     "default",      # TODO-FRASE: default (caso padrão)

    # --- extras (não obrigatórios pelo enunciado) ---
    "ENQUANTO":   "Dormindo no gelo e acordando suado",           # while
    "IMPRIME":    "Vou botar uma gravata pra te ouvir",           # print
}

# ---------------------------------------------------------------
# Mensagens (a "piada" aparece ANTES do erro técnico)
# ---------------------------------------------------------------
PIADA_ERRO_LEXICO = (
    "Eu não sei nada de tudo, eu nunca consegui falar com o cavalo, "
    "eu paro, falo com ele e ele não me responde. Futebol é meu forte."
)
PIADA_ERRO_SINTATICO = (
    "Tu comprou o cavalo pra ler ou pra correr? "
    "Porque se for pra ler está desfeito o negócio"
)
PIADA_ERRO_SEMANTICO = (          # variável não declarada, redeclaração, etc.
    "Não pode querer ir pra guerra com secador de cabelo"
)
PIADA_ERRO_TIPOS = (              # incompatibilidade de tipos na atribuição
    "Não dá pra servir farofa em restaurante com ventilador de teto"
)
PIADA_SUCESSO = (                 # programa aceito sem erros
    "Se Beleza fosse crime, eu seria inocente"
)
