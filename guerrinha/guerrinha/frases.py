# -*- coding: utf-8 -*-
"""
=====================================================================
  frases.py  —  ÚNICO ARQUIVO ONDE SE TROCAM PALAVRAS E MENSAGENS
=====================================================================

Tudo que é "texto do Little_Guerra" mora aqui. O analisador léxico monta
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
NOME_LINGUAGEM = "Little_Guerra"  # nome da linguagem
EXTENSAO = ".grr"                 # extensão dos programas-fonte

# ---------------------------------------------------------------
# Palavras reservadas  (TOKEN -> frase)
# ---------------------------------------------------------------
# A chave (à esquerda) é o nome do token usado na gramática
# (guerrinha/parser.py). NÃO mude as chaves, só as frases.
PALAVRAS_RESERVADAS = {
    # --- tipos (construção a) ---
    "TIPO_INT":   "radio",        # tipo inteiro
    "TIPO_FLOAT": "gaucha",       # tipo fracionário

    # --- condicional (construção b) ---
    "SE":         "Ninguém quer saber o preço do dólar",          # if
    "SENAOSE":    "Se algo deu certo, então tem que mudar",       # else if
    "SENAO":      ", nós não temos dólar",                        # else

    # --- seleção múltipla (construção c) ---
    "ESCOLHA":    "O time vai jogar motivado?",   # switch
    "CASO":       "Então vai perder motivado",    # case
    "PARE":       "Tem gato na tuba",             # break (encerramento de caso)
    "PADRAO":     "Butuca tira boi do mato",      # default (caso padrão)

    # --- extras (não obrigatórios pelo enunciado) ---
    "ENQUANTO":   "Não dá pra comer banana e assobiar ao mesmo tempo",  # while
    "IMPRIME":    "Vou botar uma gravata pra te ouvir",                 # print
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
# Erro ao RODAR o programa (divisão por zero, variável sem valor).
# Vazio = a mensagem sai sem frase antes.
PIADA_ERRO_EXECUCAO = "Dormindo no gelo e acordando suado"
