# Setup

## Requisitos locais

- Python 3.12 ou superior
- pip
- Docker Desktop opcional para execução containerizada

## Instalação local

```powershell
cd "C:\programacao\tarefa-08-projeto-final"
python -m pip install -r requirements.txt
```

## Execução local

```powershell
python run-pipeline.py
```

## Execução com Docker

```bash
docker build -t ip-enricher:latest .
docker run --rm \
  -v "$(pwd)/config.yaml:/app/config.yaml:ro" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/logs:/app/logs" \
  ip-enricher:latest
```
