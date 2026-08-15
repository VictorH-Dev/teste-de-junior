# Tarefa 04 - Containerização do Coletor

## Objetivo

Containerizar o monitor de URLs criado na Tarefa 3, usando Dockerfile, Docker Compose, volumes e um script de execução.

## O que foi implementado

- `Dockerfile` usando imagem oficial `python:3.12-slim`.
- Usuário não-root dentro do container.
- Instalação das dependências via `requirements.txt`.
- `docker-compose.yml` com volumes para:
  - `config.yaml`
  - pasta `output`
  - pasta `logs`
- Variável de ambiente `CONFIG_PATH` para indicar o caminho do arquivo de configuração dentro do container.
- Script `run.sh` com `set -euo pipefail`.
- `.dockerignore` para evitar enviar arquivos desnecessarios para a imagem.

## Como executar

No Git Bash:

```bash
cd /c/programacao/tarefa-04
chmod +x run.sh
./run.sh
```

Ou diretamente com Docker Compose:

```bash
cd /c/programacao/tarefa-04
docker compose build
docker compose up --abort-on-container-exit
```

## Arquivos gerados

Depois da execução, o container grava:

- Logs em `logs/monitor.log`.
- Resultado JSON em `output/monitor_results_YYYYMMDD_HHMMSS.json`.

## Observação sobre teste local

Durante o teste local, tentei executar o fluxo pelo Git Bash:

```bash
cd /c/programacao/tarefa-04
chmod +x run.sh
./run.sh
```

O Docker Desktop abriu, mas apresentou um problema relacionado ao WSL:

```text
There was a problem with WSL
An error occurred while running a WSL command.
Wsl/Service/RegisterDistro/CreateVm/HCS/ERROR_NOT_FOUND
```

Pelo erro, o problema parece estar na configuração local do WSL/Docker Desktop, não necessariamente nos arquivos da aplicação. Como alternativa, validei o funcionamento do monitor diretamente com Python:

```powershell
cd "C:\programacao\tarefa-04"
python monitor.py
```

Resultado obtido:

```text
Monitoramento concluido.
Total de URLs: 3
Sucesso: 3
Falhas: 0
```

Com isso, a aplicação Python foi validada, e os arquivos de containerização ficaram preparados para execução em um ambiente com Docker e WSL configurados corretamente.

## Como explicar esta tarefa

Nesta tarefa, eu peguei o monitor da Tarefa 3 e preparei ele para rodar dentro de um container Docker. A ideia é que qualquer pessoa consiga executar o projeto sem configurar tudo manualmente na máquina. O Dockerfile monta a imagem com Python e dependências, o Docker Compose organiza os volumes de configuração, logs e saída, e o script `run.sh` automatiza o build e a execução.
