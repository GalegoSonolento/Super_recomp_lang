# Guia da linguagem Guerrinha

> Arquivo gerado por `ferramentas/gerar_guia.py` a partir de `guerrinha/frases.py`. **Não edite à mão**: rode o script de novo depois de trocar uma frase. Todos os exemplos abaixo foram compilados.

## 1. Palavras reservadas

| Construção | Escreva exatamente |
|---|---|
| tipo inteiro | `int` |
| tipo fracionário | `float` |
| se (if) | `Ninguém quer saber o preço do dólar` |
| senão-se (else if) | `Se algo deu certo, então tem que mudar` |
| senão (else) | `, nós não temos dólar` |
| seleção (switch) | `switch` |
| caso (case) | `case` |
| encerramento (break) | `break` |
| caso padrão (default) | `default` |
| laço (while) | `Dormindo no gelo e acordando suado` |
| impressão (print) | `Vou botar uma gravata pra te ouvir` |

Regras de escrita das frases:
- **Maiúsculas e minúsculas contam.** Copie a frase exatamente.
- Entre palavras da frase pode ter quantos espaços quiser, até quebra de linha.
- Ao redor de pontuação (`,` `?`) o espaço é opcional.
- Acentos **só** existem dentro das frases. Variáveis são ASCII.

## 2. Estrutura de um programa

Um programa é uma sequência de comandos, sem `main`. Todo comando simples termina em `;`. Comentários vão de `//` até o fim da linha.

```
// meu primeiro programa
int x = 1;
Vou botar uma gravata pra te ouvir (x + 1);
```

## 3. Declarações

Dois tipos: `int` (inteiro) e `float` (fracionário). Dá para declarar uma variável por vez ou uma lista, com ou sem valor inicial.

```
int a;
int b, c = 2, d;
float media = 0.0, taxa = 3;     // int -> float é permitido
```

- Variável: começa com letra ou `_`, depois letras, dígitos ou `_` (sem acento).
- Literal fracionário precisa de dígito dos dois lados do ponto: `0.5`, e não `.5` nem `5.`.
- Cada nome só pode ser declarado uma vez, considerando o bloco atual e os blocos externos.

## 4. Atribuição e expressões

`variavel = expressao;` — a variável precisa ter sido declarada antes.

| Prioridade | Operadores | Associa |
|---|---|---|
| maior | `-` unário | direita |
| média | `*` `/` | esquerda |
| menor | `+` `-` | esquerda |

```
int x, y = 4;
float f;
x = 10 + 5 * 2;        // 20
x = 20 - 4 - 1;        // (20 - 4) - 1 = 15
x = -(y + 1) * 2;      // -10
f = y / 3;             // int / int = 1, depois vira 1.0
f = y / 3.0;           // float: 1.333...
```

Regras de tipo:
- `int op int` → int (a divisão **trunca**); se houver qualquer float → float.
- `float ← int`: ok, com conversão automática (aparece como `(float)` no TAC).
- `int ← float`: **erro**.

```
int n;
n = 2.5;
```

Saída:
```
[Guerrinha] Erro semântico na linha 2: não é possível atribuir valor float à variável int 'n'.
```

## 5. Condições

Seis operadores: `==` `!=` `>` `<` `>=` `<=`. Uma condição compara **duas expressões** e só aparece dentro de `( )` do se, do senão-se e do laço. Não existe `&&`, `||` nem `!`, e não dá para encadear (`a < b < c`).

## 6. Condicional

Chaves são **obrigatórias**, mesmo com um comando só. Senão-se e senão são opcionais; pode haver vários senão-se e no máximo um senão, sempre por último.

```
int a = 7;
float r;

Ninguém quer saber o preço do dólar (a > 10) {
    r = 1.0;
} Se algo deu certo, então tem que mudar (a == 7) {
    r = 2.0;
}, nós não temos dólar {
    r = 0.0;
}
```

Repare que a frase do senão começa com vírgula: escreva `}, nós não temos dólar {`.

Código de três endereços gerado para esse exemplo:

```
    a = 7
    ifFalse a > 10 goto L2
    r = 1.0
    goto L1
L2:
    ifFalse a == 7 goto L3
    r = 2.0
    goto L1
L3:
    r = 0.0
L1:
```

## 7. Seleção múltipla

- A expressão entre `( )` precisa ser **int**.
- Cada caso tem um ou mais rótulos **literais inteiros** separados por vírgula (pode ser negativo: `-1`).
- Rótulo repetido no mesmo comando é erro.
- Sem `break;` o fluxo **cai no próximo caso** (como em C).
- O caso padrão é opcional e, se existir, vem **por último**.
- É preciso pelo menos um caso comum.

```
int dia = 3, tipo;

switch (dia) {
    case 1:
        tipo = 10;
        break;
    case 2, 6, 7:
        tipo = 20;
        break;
    case 3:
        tipo = 30;        // sem encerramento: continua no próximo caso
    case 4:
        tipo = tipo + 1;
        break;
    default:
        tipo = 0;
}
```

## 8. Laço

`break;` dentro do laço sai dele.

```
int i = 0;
Dormindo no gelo e acordando suado (i < 10) {
    Ninguém quer saber o preço do dólar (i == 5) {
        break;
    }
    i = i + 1;
}
```

## 9. Impressão

Recebe **uma** expressão entre parênteses.

```
int x = 3;
Vou botar uma gravata pra te ouvir (x * 2 + 1);
```

## 10. Escopo

Cada `{ }` abre um escopo novo. O que é declarado dentro do bloco não existe fora dele, e um nome de fora não pode ser redeclarado dentro. Todos os casos de uma seleção compartilham o mesmo escopo.

```
int a = 1;
Ninguém quer saber o preço do dólar (a > 0) {
    int local = 2;
}
a = local;
```

Saída:
```
[Guerrinha] Erro semântico na linha 5: variável 'local' não foi declarada.
```

## 11. O que dá erro

| Fase | Situação | Exemplo |
|---|---|---|
| léxico | caractere fora do alfabeto | `a = b @ 2;` |
| léxico | variável com acento / frase digitada errado | `preço = 1;` |
| sintático | falta `;` (o erro aparece na linha **seguinte**) | `a = 1` |
| sintático | bloco sem chaves | `Ninguém quer saber o preço do dólar (a > 1) a = 2;` |
| sintático | padrão antes de um caso comum | ver seção 7 |
| sintático | condição fora de se/laço | `a = b > 1;` |
| semântico | variável não declarada | `x = 1;` |
| semântico | redeclaração | `int a; int a;` |
| semântico (tipos) | `int ← float` | `n = 2.5;` |
| semântico (tipos) | seleção sobre float | `switch (f) ...` |
| semântico | rótulo de caso repetido | `case 1: ... case 2, 1:` |
| semântico | encerramento fora de seleção/laço | `break;` solto |

Erro léxico ou sintático interrompe a compilação (para no **primeiro** erro sintático). Os erros semânticos são todos listados de uma vez.

## 12. Escrevendo um programa novo

1. Crie um arquivo `.grr` em UTF-8.
2. Rode `python main.py meu_programa.grr`. Opções: `--so-tac`, `--so-ast` e `--tokens`; esta última é ótima para descobrir por que uma frase não foi reconhecida.
3. Para virar teste do trabalho:
   - válido → `testes/validos/vN_descricao.grr`; inválido → `testes/invalidos/<tipo>N_descricao.grr` (`s` sintático, `l` léxico, `e` semântico);
   - comece com o cabeçalho abaixo (ele entra no relatório);
   - rode `python ferramentas/rodar_testes.py` (a saída vai para `testes/saidas/`);
   - rode `python ferramentas/gerar_notebook.py` para atualizar o Colab.

```
// E4 - ERRO SEMÂNTICO: <o que este programa testa>.
// Esperado: <aceito | erro X na linha N>.
```
