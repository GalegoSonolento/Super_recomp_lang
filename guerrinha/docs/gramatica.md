# Gramática (BNF)

Escrita com os **nomes dos tokens**; a frase de cada palavra reservada está em
`guerrinha/frases.py` (tabela: `python main.py --palavras`). É a mesma gramática
das docstrings de `guerrinha/parser.py`. Símbolo inicial: `programa`. `ε` = vazio.

```bnf
programa      ::= lista_cmd

lista_cmd     ::= lista_cmd cmd
                | ε

cmd           ::= declaracao | atribuicao | se | escolha
                | enquanto | imprime | pare

bloco         ::= ABRE_CHAVE lista_cmd FECHA_CHAVE

(* (a) declarações *)
declaracao    ::= tipo lista_decl PONTO_VIRGULA
tipo          ::= TIPO_INT | TIPO_FLOAT
lista_decl    ::= lista_decl VIRGULA item_decl
                | item_decl
item_decl     ::= ID
                | ID ATRIBUI expr

(* (e) atribuição *)
atribuicao    ::= ID ATRIBUI expr PONTO_VIRGULA

(* (b) condicional *)
se            ::= SE ABRE_PAR condicao FECHA_PAR bloco lista_senaose senao_opt
lista_senaose ::= lista_senaose SENAOSE ABRE_PAR condicao FECHA_PAR bloco
                | ε
senao_opt     ::= SENAO bloco
                | ε

(* laço — extra *)
enquanto      ::= ENQUANTO ABRE_PAR condicao FECHA_PAR bloco

(* (c) seleção múltipla *)
escolha       ::= ESCOLHA ABRE_PAR expr FECHA_PAR
                  ABRE_CHAVE lista_casos padrao_opt FECHA_CHAVE
lista_casos   ::= lista_casos caso
                | caso
caso          ::= CASO lista_rotulos DOIS_PONTOS lista_cmd
lista_rotulos ::= lista_rotulos VIRGULA rotulo
                | rotulo
rotulo        ::= NUM_INT
                | MENOS NUM_INT
padrao_opt    ::= PADRAO DOIS_PONTOS lista_cmd
                | ε
pare          ::= PARE PONTO_VIRGULA

(* saída — extra *)
imprime       ::= IMPRIME ABRE_PAR expr FECHA_PAR PONTO_VIRGULA

(* (f) condições *)
condicao      ::= expr relop expr
relop         ::= IGUAL | DIFERENTE | MAIOR | MENOR | MAIOR_IGUAL | MENOR_IGUAL

(* (d) expressões — ambígua, desambiguada pela tabela de precedência *)
expr          ::= expr MAIS expr
                | expr MENOS expr
                | expr VEZES expr
                | expr DIVIDE expr
                | MENOS expr            %prec MENOS_UNARIO
                | ABRE_PAR expr FECHA_PAR
                | NUM_INT | NUM_FLOAT | ID
```

## Precedência (menor → maior)

| Nível | Operadores | Associatividade |
|---|---|---|
| 1 | `+` `-` | esquerda |
| 2 | `*` `/` | esquerda |
| 3 | `-` unário | direita |

Relacionais não entram na tabela: só aparecem em `condicao`, nunca encadeados.

## Tokens

| Token | Lexema |
|---|---|
| `ID` | `[A-Za-z_][A-Za-z0-9_]*` (sem acento) |
| `NUM_INT` | `\d+` |
| `NUM_FLOAT` | `\d+\.\d+` |
| `MAIS` `MENOS` `VEZES` `DIVIDE` | `+` `-` `*` `/` |
| `IGUAL` `DIFERENTE` | `==` `!=` |
| `MAIOR` `MENOR` `MAIOR_IGUAL` `MENOR_IGUAL` | `>` `<` `>=` `<=` |
| `ATRIBUI` | `=` |
| `PONTO_VIRGULA` `VIRGULA` `DOIS_PONTOS` | `;` `,` `:` |
| `ABRE_PAR` `FECHA_PAR` `ABRE_CHAVE` `FECHA_CHAVE` | `(` `)` `{` `}` |
| comentário (descartado) | `//` até o fim da linha |
| palavras reservadas | ver `guerrinha/frases.py` |

## Conflitos

- **Com** a tabela de precedência: 0 shift/reduce, 0 reduce/reduce.
- **Sem** ela: 16 shift/reduce, todos nos estados de `expr op expr`
  (`python ferramentas/experimento_conflitos.py`; detalhes em `build/sem_precedencia.out`).
- Sem *dangling else*: os blocos exigem chaves.
