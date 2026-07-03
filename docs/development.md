# Development Documentation

## Arquitetura do Projeto

O **ipynbcleaner** é um pacote Python organizado da seguinte forma:

```
ipynbcleaner/
├─ src/
│   └─ ipynbcleaner/
│       ├─ __init__.py
│       ├─ cleaner.py        # Lógica principal de limpeza de notebooks
│       ├─ cli.py            # Interface de linha de comando (argparse)
│       └─ metrics.py        # Cálculo de métricas (contagem de células, linhas, etc.)
├─ tests/
│   └─ test_cleaner.py      # Testes unitários
├─ docs/                     # Documentação técnica
│   ├─ backlog.md
│   ├─ development.md       # <--- este arquivo
│   └─ release.md
├─ scripts/                  # Scripts auxiliares (release, CI)
├─ README.md
├─ pyproject.toml
└─ ...
```

### Principais Componentes

* **cleaner.py** – Funções para remover células vazias, limpar metadados e normalizar o layout.
* **cli.py** – Função `main()` que expõe a CLI via `python -m ipynbcleaner` ou o console script `ipynbcleaner`.
* **metrics.py** – Calcula estatísticas como número de células, linhas de código, tamanho do notebook, etc.
* **tests/** – Cobertura de funcionalidades críticas usando `unittest`.

### Fluxo de Trabalho

1. **Leitura do notebook** (`nbformat.read`).
2. **Aplicação das regras de limpeza** (`clean_notebook`).
3. **Opcional: cálculo de métricas** (`calculate_metrics`).
4. **Escrita do notebook limpo** (`nbformat.write`).

### Extensibilidade

- Novas regras podem ser adicionadas em `cleaner.py` como funções que recebem e retornam um `NotebookNode`.
- O CLI aceita argumentos para selecionar quais regras aplicar.
- O módulo `metrics` pode ser estendido para novos tipos de análise (ex.: contagem de imports).

---

## Guia de Contribuição

1. Fork o repositório.
2. Crie uma branch `feature/<descrição>`.
3. Siga o padrão de commits **Conventional Commits**.
4. Execute os testes com `pytest` antes de submeter o PR.
5. Atualize a documentação quando necessário.

---

*Este documento será mantido atualizado à medida que novas funcionalidades forem adicionadas.*
