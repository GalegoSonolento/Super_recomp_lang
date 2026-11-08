# Guerrinha — Compiladores, Trabalho do Grau B

Linguagem cujas palavras reservadas são frases do Adroaldo Guerra Filho (Rádio Gaúcha).
Front-end completo em **Python + PLY**: léxico → sintático (LALR) → semântico → tradução (AST + código de três endereços).

> **Falta trocar algumas palavras:** veja [`SUBSTITUICOES.md`](SUBSTITUICOES.md).

## Como rodar

```bash
pip install ply                               # uma vez
python main.py testes/validos/v4_programa_completo.grr
python ferramentas/rodar_testes.py            # todos os testes -> testes/saidas/
```

Outras opções do `main.py`: `--so-ast`, `--so-tac`, `--tokens`, `--palavras`, `--debug` (grava `build/parser.out`).

**Colab:** rode `python ferramentas/gerar_notebook.py`, suba `colab/Guerrinha.ipynb` no Colab e use *Executar tudo*. O notebook é autossuficiente (cada arquivo vira uma célula `%%writefile`).

## Estrutura

```
guerrinha/
  frases.py        <- ÚNICO lugar para trocar palavras reservadas e mensagens
  lexer.py         analisador léxico (gera as regex a partir das frases)
  parser.py        gramática + ações semânticas que constroem a AST
  ast_nodes.py     nós da AST + impressão
  semantica.py     declaração antes do uso, tipos, escopo, break, rótulos
  tac.py           geração de código de três endereços
  erros.py         formato das mensagens (piada + erro + linha)
main.py            CLI: executa as fases em sequência
testes/
  validos/         v1..v4   (devem ser aceitos)
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
| 2a declarações (int/float, lista) | `p_declaracao`, `p_lista_decl` em `parser.py` |
| 2b condicional + alternativo opcional | `p_se`, `p_lista_senaose`, `p_senao_opt` |
| 2c seleção múltipla | `p_escolha`, `p_caso`, `p_lista_rotulos`, `p_padrao_opt`, `p_pare` |
| 2d expressões com precedência | `precedence` + `p_expr_*` |
| 2e atribuição com delimitador | `p_atribuicao` (`;`) |
| 2f seis relacionais | `p_condicao` |
| 3c semântica com linha | `semantica.py` |
| 3d tradução dirigida | AST nas ações de `parser.py`; TAC em `tac.py` |
| 3e 4 válidos + 4 inválidos | `testes/` (4 + 7) |
| Erros com linha | `erros.py` (todas as fases) |

## Pendências do trabalho
- [ ] Trocar as palavras provisórias (`SUBSTITUICOES.md`) e batizar a linguagem
- [ ] Gerar o notebook e testar no Colab
- [ ] Gravar o vídeo (≤ 1 min, MP4): válido → TAC → inválido sintático → inválido semântico
- [ ] Preencher o relatório (`docs/referencia/...Template...docx`) usando `docs/` e `testes/saidas/`
- [ ] Declarar o uso de IA na seção 6 do relatório
