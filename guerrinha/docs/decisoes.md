# Decisões de projeto

Formato: **decisão** → benefício · por quê · contraponto. Serve de base para a seção 3 do relatório.

1. **Python + PLY** (e não JS, Lark ou Flex/Bison)
   - Benefício: separa léxico e sintático como Flex/Bison, gera `parser.out` com a tabela LALR e os conflitos, e roda no Colab com `pip install ply`.
   - Por quê: o enunciado só aceita Flex/Bison, PLY ou Lark (JS não é opção). PLY é o que mais mostra conflitos e precedência, que valem 3,0.
   - Contra: o PLY não é mais publicado no PyPI (a versão do pip é a 3.11, de 2018). Lark tem mensagens de erro melhores e uma gramática única mais enxuta.

2. **Palavras reservadas = frases, montadas a partir de um dicionário** (`frases.py`)
   - Benefício: trocar uma palavra é editar uma string. O léxico gera as regex sozinho.
   - Por quê: com frases, o truque clássico de "reconhece ID e consulta a tabela" não funciona, porque uma frase tem vários lexemas.
   - Contra: a regex fica grande e a ordem importa. Uma frase escrita errado vira uma sequência de IDs e dá erro léxico ou sintático, não "palavra reservada errada".

3. **Diferencia maiúsculas de minúsculas; espaço flexível dentro das frases**
   - Benefício: regra simples de explicar e de especificar no léxico.
   - Contra: `ninguém quer saber...` (com minúscula) é rejeitado.

4. **Identificadores só em ASCII**
   - Benefício: o acento é exclusivo das frases. Uma frase digitada errado dá uma mensagem clara por palavra.
   - Contra: não dá para declarar `preço`.

5. **Gramática de expressões ambígua + tabela `precedence`** (e não `expr/termo/fator`)
   - Benefício: gramática curta, e o relatório pode mostrar os 16 conflitos que somem com a tabela.
   - Contra: a precedência fica fora da gramática. A versão estratificada a deixaria explícita na BNF.

6. **Blocos com chaves obrigatórias**
   - Benefício: elimina o *dangling else* (0 conflitos no `se`).
   - Contra: perde a chance de discutir esse conflito clássico no relatório.

7. **"Senão-se" como palavra própria (`SENAOSE`)**
   - Benefício: usa a frase "Se algo deu certo..." e gera um TAC com um único rótulo de saída para a cadeia toda.
   - Contra: um token a mais. `senão { se ... }` já teria o mesmo efeito.

8. **Seleção múltipla com fallthrough (estilo C)**
   - Benefício: dá sentido ao "encerramento de caso" pedido no enunciado, e o TAC mostra a diferença.
   - Contra: esquecer o `pare` é um bug clássico. O padrão precisa vir por último (regra sintática).

9. **Para no 1º erro sintático, mas relata todos os léxicos e semânticos**
   - Benefício: evita erros sintáticos em cascata e mostra vários erros semânticos de uma vez nos testes.
   - Contra: não há recuperação de erro (`error` do yacc), então o usuário corrige um erro sintático por vez.

10. **Tipos: `float ← int` permitido, `int ← float` erro; `int / int = int`**
    - Benefício: igual a C/Java, e o TAC mostra a conversão `(float)` explicitamente.
    - Contra: `media = limite / 2` trunca antes de alargar (ver teste V1).

11. **Escopo por bloco, sem sombreamento**
    - Benefício: testes mais interessantes (variável local usada fora do bloco). Os nomes no TAC continuam únicos por escopo visível.
    - Contra: mais código do que uma tabela global.

12. **Tradução: AST (nas ações do parser) + código de três endereços (a partir da AST)**
    - Benefício: cumpre "AST impressa" e "TAC", duas das três opções. O TAC de `se`/`escolha`/`enquanto` mostra o controle de fluxo.
    - Contra: o TAC sai de um segundo passe sobre a AST, não direto das ações. Se o professor exigir "na ação", é preciso explicar que a AST é a tradução dirigida.

13. **Frases de erro em vez de try/catch e main**
    - Benefício: try/catch exigiria semântica de exceção em tempo de execução, que um front-end não demonstra. O enunciado aceita programa sem `main` (exemplo Beacon).
    - Contra: perde duas construções "temáticas". Dá para voltar com `main` facilmente: `programa ::= MAIN bloco`.
