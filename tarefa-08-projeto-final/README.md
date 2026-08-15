# Tarefa 08 - Projeto Integrado Final

## Objetivo

Criar um pipeline completo de enriquecimento de IPs, juntando coleta em API pública, processamento, classificação, Docker, automação e documentação.

## Componentes

- `collector.py`: consulta a API `ip-api.com` e enriquece os IPs com geolocalização, ISP, organização e ASN.
- `processor.py`: lê o resultado da coleta e classifica os IPs.
- `run-pipeline.py`: executa coleta e processamento em sequência.
- `Dockerfile`: prepara a aplicação para rodar em container.
- `docker-compose.yml`: organiza volumes de configuração, saída e logs.
- `run-pipeline.sh`: automatiza build e execução via Docker.
- `docs/`: documentação de arquitetura, setup e uso.

## Como executar localmente

```powershell
cd "C:\programacao\tarefa-08-projeto-final"
python -m pip install -r requirements.txt
python run-pipeline.py
```

## Como executar com Docker

```bash
cd /c/programacao/tarefa-08-projeto-final
chmod +x run-pipeline.sh
./run-pipeline.sh
```

## Arquivos gerados

- `output/enriched_ips.json`
- `output/final_report.json`
- `logs/pipeline.log`

## Observação

O Docker depende do Docker Desktop e do WSL configurados corretamente no Windows. Caso o ambiente local tenha problema com WSL, o pipeline ainda pode ser validado diretamente com Python.
