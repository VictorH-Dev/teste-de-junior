# Tarefa 07 - Git Workflow e Automação

## Objetivo

Simular um fluxo real de desenvolvimento usando Git, branches, commits no padrão Conventional Commits, merge e geração de changelog.

## O que foi implementado

- Script `git-workflow.sh` com `set -euo pipefail`.
- Inicialização de repositório Git local.
- Criação da branch `main`.
- Criação da branch `feat/health-check-endpoint`.
- Commit inicial com script simples de health check.
- Implementação da classe `HealthChecker`.
- Commit de feature usando Conventional Commits.
- Merge da branch de feature para `main`.
- Criação do `CHANGELOG.md`.
- Arquivo `output.log` com exemplo do histórico Git gerado.

## Como executar

Em um ambiente com Bash disponível:

```bash
cd /c/programacao/tarefa-07
chmod +x git-workflow.sh
./git-workflow.sh
```

## Como testar o código Python

No PowerShell:

```powershell
cd "C:\programacao\tarefa-07"
python -m pip install -r requirements.txt
python healthcheck.py
```

## Observação sobre teste local

Na minha máquina, o comando `bash --version` tentou usar o WSL, mas o WSL não possui uma distribuição Linux instalada. Por isso, não consegui executar o script Bash diretamente neste ambiente.

Mesmo assim, validei o fluxo Git usando comandos Git equivalentes no PowerShell e deixei o script `git-workflow.sh` pronto para rodar em um ambiente com Bash configurado.

Ao tentar rodar a tarefa pelo caminho esperado, encontrei a mesma limitação de ambiente relacionada ao Bash/WSL. A dificuldade foi documentada para deixar claro o que foi tentado e qual alternativa foi usada para validar a entrega.

## Como explicar esta tarefa

Nesta tarefa, eu simulei um fluxo de trabalho com Git. A ideia foi começar com um arquivo simples, criar uma branch de feature, implementar uma classe de health check, fazer commit seguindo o padrão Conventional Commits e depois fazer merge para a branch principal.

Também gerei um changelog para registrar a nova funcionalidade. Isso mostra um fluxo parecido com o usado em equipes reais, onde cada mudança fica organizada em branch, commit e histórico.
