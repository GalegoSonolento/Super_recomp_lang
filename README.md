# Guerrinha Lang — Compiladores, Trabalho do Grau B

Linguagem cujas palavras reservadas são frases do Adroaldo Guerra Filho (Rádio Gaúcha).
Compilador em **Python + PLY**: léxico → sintático (LALR) → semântico → tradução (AST + código de três endereços) → execução (interpretador do código de três endereços).

## Como rodar um arquivo `.grr`

1. **Instale o pré-requisito** (uma vez só). Precisa do Python 3 e do PLY:
   ```bash
   pip install ply
   ```
2. **Entre na pasta do compilador**, a que tem o `main.py`:
   ```bash
   cd guerrinha
   ```
3. **Escreva o programa** num arquivo `.grr` salvo em UTF-8, por exemplo `meu_programa.grr`:
   ```
   radio x = 2;
   Vou botar uma gravata pra te ouvir ("Resultado:");
   Vou botar uma gravata pra te ouvir (x * 10 + 1);
   ```
   As palavras reservadas estão em `python main.py --palavras`, e a linguagem inteira está explicada em [`../guia_da_linguagem.md`](../guia_da_linguagem.md).
4. **Rode o programa**. Ele é compilado e executado:
   ```bash
   python main.py meu_programa.grr
   ```
   ```
   Resultado:
   21
   ```
   O caminho do arquivo é relativo à pasta atual. Para rodar um teste: `python main.py testes/validos/v5_hello_world.grr`.
5. **Se der erro**, nada é executado. Aparece a frase e o erro com a linha. Por exemplo, usando `y` sem declarar:
   ```
     >> "Não pode querer ir pra guerra com secador de cabelo"
     [Little_Guerra] Erro semântico na linha 3: variável 'y' não foi declarada.
   ```
   Corrija a linha indicada e rode de novo.
6. **Opcional**: veja a tradução ou grave a saída em arquivo:
   ```bash
   python main.py meu_programa.grr -c        # mostra AST + código de três endereços (não executa)
   python main.py meu_programa.grr --so-tac  # mostra só o código de três endereços
   python main.py meu_programa.grr -gt       # executa e grava meu_programa.txt ao lado do .grr
   ```

## Outros comandos

```bash
pip install ply                                     # uma vez
python main.py testes/validos/v5_hello_world.grr    # compila e EXECUTA
python ferramentas/rodar_testes.py                  # todos os testes -> testes/saidas/
```

Se o programa tiver erro (léxico, sintático, semântico ou de execução), aparece a frase + o erro com a linha, e o código de saída é 1.

| Opção do `main.py` | O que faz |
|---|---|
| *(nenhuma)* | compila e executa |
| `-gt`, `--gentxt` | também grava `programa.txt` ao lado do `.grr`, com AST + TAC (ou os erros), no mesmo formato de `testes/saidas/` |
| `-c`, `--compilar` | só compila: mostra AST + TAC no terminal, não executa |
| `--so-ast`, `--so-tac` | só compila: mostra só a AST / só o TAC |
| `--tokens` | lista os tokens reconhecidos |
| `--palavras` | tabela de palavras reservadas |
| `--debug` | grava `build/parser.out` (tabela LALR) |

No Windows, se os acentos saírem quebrados no terminal, rode antes `$env:PYTHONIOENCODING = "utf-8"` (PowerShell).

**Colab:** rode `python ferramentas/gerar_notebook.py`, suba `colab/Little_Guerra.ipynb` no Colab e use *Executar tudo*. O notebook é autossuficiente (cada arquivo vira uma célula `%%writefile`).

## Estrutura

```
guerrinha/
  frases.py        <- ÚNICO lugar para trocar palavras reservadas e mensagens
  lexer.py         analisador léxico (gera as regex a partir das frases)
  parser.py        gramática + ações semânticas que constroem a AST
  ast_nodes.py     nós da AST + impressão
  semantica.py     declaração antes do uso, tipos, escopo, break, rótulos
  tac.py           geração de código de três endereços
  interpretador.py executa o código de três endereços (faz o programa rodar)
  erros.py         formato das mensagens (piada + erro + linha)
main.py            CLI: compila e executa (ver opções acima)
testes/
  validos/         v1..v5   (devem ser aceitos)
  invalidos/       s* sintáticos, l* léxico, e* semânticos (devem ser rejeitados)
  saidas/          gerado por rodar_testes.py (vai para o relatório)
ferramentas/
  rodar_testes.py          roda tudo e confere aceito/rejeitado
  experimento_conflitos.py conflitos com e sem tabela de precedência
  trocar_palavra.py        troca palavra provisória nos testes
  gerar_notebook.py        gera colab/<Nome>.ipynb
docs/
  gramatica.md     BNF, precedência, tokens, conflitos   (relatório seção 2)
  decisoes.md      decisões com benefício/contraponto    (relatório seção 3)
  referencia/      enunciado e template do relatório
```

## Mapa enunciado → código

| Requisito | Onde |
|---|---|
| 2a declarações (radio/gaucha, lista) | `p_declaracao`, `p_lista_decl` em `parser.py` |
| 2b condicional + alternativo opcional | `p_se`, `p_lista_senaose`, `p_senao_opt` |
| 2c seleção múltipla | `p_escolha`, `p_caso`, `p_lista_rotulos`, `p_padrao_opt`, `p_pare` |
| 2d expressões com precedência | `precedence` + `p_expr_*` |
| 2e atribuição com delimitador | `p_atribuicao` (`;`) |
| 2f seis relacionais | `p_condicao` |
| 3c semântica com linha | `semantica.py` |
| 3d tradução dirigida | AST nas ações de `parser.py`; TAC em `tac.py` |
| 3e 4 válidos + 4 inválidos | `testes/` (5 + 9) |
| Erros com linha | `erros.py` (todas as fases) |

## Pendências do trabalho
- [x] Trocar as palavras provisórias (`SUBSTITUICOES.md`) e batizar a linguagem
- [ ] Gerar o notebook e testar no Colab
- [ ] Gravar o vídeo (≤ 1 min, MP4): válido → TAC → inválido sintático → inválido semântico
- [ ] Preencher o relatório (`docs/referencia/...Template...docx`) usando `docs/` e `testes/saidas/`
- [ ] Declarar o uso de IA na seção 6 do relatório
