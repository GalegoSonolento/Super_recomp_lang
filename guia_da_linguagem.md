# Guia da linguagem Guerrinha

## 1. Palavras reservadas

| Construção | Escreva exatamente |
|---|---|
| tipo inteiro | `radio` |
| tipo fracionário | `gaucha` |
| se (if) | `Ninguém quer saber o preço do dólar` |
| senão-se (else if) | `Se algo deu certo, então tem que mudar` |
| senão (else) | `, nós não temos dólar` |
| seleção (switch) | `O time vai jogar motivado?` |
| caso (case) | `Então vai perder motivado` |
| encerramento (break) | `Tem gato na tuba` |
| caso padrão (default) | `Butuca tira boi do mato` |
| laço (while) | `Não dá pra comer banana e assobiar ao mesmo tempo` |
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
radio x = 1;
Vou botar uma gravata pra te ouvir (x + 1);
```

## 3. Declarações

Dois tipos: `radio` (inteiro) e `gaucha` (fracionário). Dá para declarar uma variável por vez ou uma lista, com ou sem valor inicial.

```
radio a;
radio b, c = 2, d;
gaucha media = 0.0, taxa = 3;    // radio -> gaucha é permitido
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
radio x, y = 4;
gaucha f;
x = 10 + 5 * 2;        // 20
x = 20 - 4 - 1;        // (20 - 4) - 1 = 15
x = -(y + 1) * 2;      // -10
f = y / 3;             // radio / radio = 1, depois vira 1.0
f = y / 3.0;           // gaucha: 1.333...
```

Regras de tipo:
- `radio op radio` → radio (a divisão **trunca**); se houver qualquer gaucha → gaucha.
- `gaucha ← radio`: ok, com conversão automática (aparece como `(float)` no TAC).
- `radio ← gaucha`: **erro**.

```
radio n;
n = 2.5;
```

Saída:
```
[Little_Guerra] Erro semântico na linha 2: não é possível atribuir valor gaucha à variável radio 'n'.
```

## 5. Condições

Seis operadores: `==` `!=` `>` `<` `>=` `<=`. Uma condição compara **duas expressões** e só aparece dentro de `( )` do se, do senão-se e do laço. Não existe `&&`, `||` nem `!`, e não dá para encadear (`a < b < c`).

## 6. Condicional

Chaves são **obrigatórias**, mesmo com um comando só. Senão-se e senão são opcionais; pode haver vários senão-se e no máximo um senão, sempre por último.

```
radio a = 7;
gaucha r;

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

- A expressão entre `( )` precisa ser **radio**.
- Cada caso tem um ou mais rótulos **literais inteiros** separados por vírgula (pode ser negativo: `-1`).
- Rótulo repetido no mesmo comando é erro.
- Sem `Tem gato na tuba;` o fluxo **cai no próximo caso** (como em C).
- O caso padrão é opcional e, se existir, vem **por último**.
- É preciso pelo menos um caso comum.

```
radio dia = 3, tipo;

O time vai jogar motivado? (dia) {
    Então vai perder motivado 1:
        tipo = 10;
        Tem gato na tuba;
    Então vai perder motivado 2, 6, 7:
        tipo = 20;
        Tem gato na tuba;
    Então vai perder motivado 3:
        tipo = 30;        // sem encerramento: continua no próximo caso
    Então vai perder motivado 4:
        tipo = tipo + 1;
        Tem gato na tuba;
    Butuca tira boi do mato:
        tipo = 0;
}
```

## 8. Laço

`Tem gato na tuba;` dentro do laço sai dele.

```
radio i = 0;
Não dá pra comer banana e assobiar ao mesmo tempo (i < 10) {
    Ninguém quer saber o preço do dólar (i == 5) {
        Tem gato na tuba;
    }
    i = i + 1;
}
```

## 9. Impressão

Recebe **uma** expressão ou **um** texto entre aspas duplas, dentro dos parênteses. O texto abre e fecha na mesma linha e não tem sequências de escape. Texto só existe aqui: não dá para guardar em variável nem juntar com número.

```
radio x = 3;
Vou botar uma gravata pra te ouvir ("Hello, World!");
Vou botar uma gravata pra te ouvir (x * 2 + 1);
```

## 10. Escopo

Cada `{ }` abre um escopo novo. O que é declarado dentro do bloco não existe fora dele, e um nome de fora não pode ser redeclarado dentro. Todos os casos de uma seleção compartilham o mesmo escopo.

```
radio a = 1;
Ninguém quer saber o preço do dólar (a > 0) {
    radio local = 2;
}
a = local;
```

Saída:
```
[Little_Guerra] Erro semântico na linha 5: variável 'local' não foi declarada.
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
| semântico | redeclaração | `radio a; radio a;` |
| semântico (tipos) | `radio ← gaucha` | `n = 2.5;` |
| semântico (tipos) | seleção sobre gaucha | `O time vai jogar motivado? (f) ...` |
| semântico | rótulo de caso repetido | `Então vai perder motivado 1: ... Então vai perder motivado 2, 1:` |
| semântico | encerramento fora de seleção/laço | `Tem gato na tuba;` solto |

Erro léxico ou sintático interrompe a compilação (para no **primeiro** erro sintático). Os erros semânticos são todos listados de uma vez.

## 12. Escrevendo um programa novo

1. Crie um arquivo `.grr` em UTF-8.
2. Rode `python main.py meu_programa.grr`: o programa é compilado e **executado** (o que ele imprime aparece no terminal). Se houver erro, aparece a frase + o erro com a linha, e nada é executado.
   Opções: `-gt` (grava `meu_programa.txt` ao lado, com AST + TAC), `-c` (só compila e mostra AST + TAC), `--so-tac`, `--so-ast` e `--tokens`; esta última é ótima para descobrir por que uma frase não foi reconhecida.
   Erros que só aparecem ao executar: divisão por zero e variável usada antes de receber valor (`radio n; ... (n + 1)`).
