# Checklist de substituições

## O que ainda falta trocar

Todas as palavras obrigatórias já foram trocadas. Só sobrou o que é opcional, em `guerrinha/frases.py`.

| # | Token (não mudar) | Construção | Provisório | Obrigatório pelo enunciado? |
|---|---|---|---|---|
| 1 | `EXTENSAO` | extensão dos fontes | `.grr` | Não |

Opcionais (são símbolos hoje; só troque se quiser):
- delimitador de comando `;`, comentário `//` → em `guerrinha/lexer.py` (`t_PONTO_VIRGULA`, `t_COMENTARIO`).
## Já definidas

| Token | Construção | Frase |
|---|---|---|
| `TIPO_INT` | tipo inteiro | radio |
| `TIPO_FLOAT` | tipo fracionário | gaucha |
| `SE` | if | Ninguém quer saber o preço do dólar |
| `SENAOSE` | else if | Se algo deu certo, então tem que mudar |
| `SENAO` | else | , nós não temos dólar |
| `ESCOLHA` | switch | O time vai jogar motivado? |
| `CASO` | case | Então vai perder motivado |
| `PARE` | break / encerramento de caso | Tem gato na tuba |
| `PADRAO` | default / caso padrão | Butuca tira boi do mato |
| `ENQUANTO` | while (extra) | Não dá pra comer banana e assobiar ao mesmo tempo |
| `IMPRIME` | print (extra) | Vou botar uma gravata pra te ouvir |
| `NOME_LINGUAGEM` | nome da linguagem | Little_Guerra |

| Mensagem | Quando aparece | Frase |
|---|---|---|
| `PIADA_ERRO_LEXICO` | caractere/palavra desconhecida | Eu não sei nada de tudo, eu nunca consegui falar com o cavalo... |
| `PIADA_ERRO_SINTATICO` | erro de sintaxe | Tu comprou o cavalo pra ler ou pra correr?... |
| `PIADA_ERRO_SEMANTICO` | não declarada, redeclarada, break fora, rótulo repetido | Não pode querer ir pra guerra com secador de cabelo |
| `PIADA_ERRO_TIPOS` | radio ← gaucha, switch com gaucha | Não dá pra servir farofa em restaurante com ventilador de teto |
| `PIADA_SUCESSO` | programa aceito | Se Beleza fosse crime, eu seria inocente |
| `PIADA_ERRO_EXECUCAO` | divisão por zero, variável sem valor (ao rodar) | Dormindo no gelo e acordando suado |

## Passo a passo para trocar uma palavra

```bash
# 1) Testes: troca no código dos .grr (comentários ficam intactos)
python ferramentas/trocar_palavra.py "switch" "Sua frase aqui"

# 2) Edite guerrinha/frases.py: "ESCOLHA": "Sua frase aqui",

# 3) Confirme e regenere o notebook do Colab
python ferramentas/rodar_testes.py
python ferramentas/gerar_notebook.py

# 4) Tabela pronta para o relatório
python main.py --palavras
```

Cuidados ao escolher frases:
- A linguagem **diferencia maiúsculas de minúsculas**: escreva no programa exatamente como em `frases.py`.
- Espaços entre palavras podem ser vários (até quebra de linha). Espaço ao redor de pontuação é opcional.
- Uma frase **não pode ser prefixo de outra** terminando em fronteira de palavra (o léxico tenta a mais longa primeiro, mas evite ambiguidade).
- Frase que começa com pontuação (como `, nós não temos dólar`) exige essa pontuação no programa: `}, nós não temos dólar {`.

## Arquivos que NÃO precisam mudar quando se troca uma frase
`lexer.py`, `parser.py`, `semantica.py`, `tac.py`, `docs/gramatica.md` (a gramática usa nomes de token, não as frases).
