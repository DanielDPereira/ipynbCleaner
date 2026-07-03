# Release Documentation

## Processo de Publicação

1. **Atualizar a versão**
   - Modifique o campo `version` no `pyproject.toml` seguindo *Semantic Versioning* (MAJOR.MINOR.PATCH).
   - Commit com a convenção `feat(release): bump version to X.Y.Z`.
2. **Construir o pacote**
   ```bash
   python -m build
   ```
   - O comando gera os artefatos `dist/*.whl` e `dist/*.tar.gz`.
3. **Testar no TestPyPI**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   - Verifique a instalação:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ ipynbcleaner
   ```
4. **Publicar no PyPI**
   ```bash
   python -m twine upload dist/*
   ```
   - Após a publicação, teste a instalação padrão:
   ```bash
   pip install ipynbcleaner
   ```

## Changelog

- Mantenha um `CHANGELOG.md` na raiz do projeto.
- Cada release deve ter uma seção com a versão, data e descrições das mudanças.

## Tags Git

- Crie uma tag anotada para cada versão lançada:
  ```bash
  git tag -a vX.Y.Z -m "Release X.Y.Z"
  git push origin vX.Y.Z
  ```

## Automação (Opcional)

- Scripts em `scripts/release.sh`/`scripts/release.ps1` podem automatizar os passos acima.
- Integre com GitHub Actions para executar a publicação ao criar um *Release*.

---

*Este documento será atualizado conforme o processo de publicação evoluir.*
