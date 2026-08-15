# Teste Técnico - Desenvolvedor Júnior

Este projeto reúne as soluções do teste técnico para a vaga de Desenvolvedor Júnior, com foco em pipelines de dados, consumo de APIs, automação, Docker e documentação.

## Estrutura

```text
C:\programacao
├── README.md
├── tarefa-01
│   ├── README.md
│   ├── collector.py
│   ├── config.json
│   ├── requirements.txt
│   └── output.json
└── tarefa-02
    ├── README.md
    ├── processor.py
    ├── input.json
    ├── requirements.txt
    ├── output.json
    └── output.csv
└── tarefa-03
    ├── README.md
    ├── monitor.py
    ├── config.yaml
    ├── requirements.txt
    ├── monitor.log
    └── monitor_results_YYYYMMDD_HHMMSS.json
└── tarefa-04
    ├── README.md
    ├── Dockerfile
    ├── docker-compose.yml
    ├── run.sh
    ├── monitor.py
    ├── config.yaml
    ├── requirements.txt
    └── .dockerignore
└── tarefa-05
    ├── README.md
    ├── auth_client.py
    ├── github_client.py
    ├── config.yaml
    ├── requirements.txt
    └── output.json
└── tarefa-06
    ├── README.md
    ├── processor.py
    ├── models.py
    ├── alerts.json
    ├── known_iocs.csv
    ├── requirements.txt
    ├── output.json
    └── output.csv
└── tarefa-07
    ├── README.md
    ├── git-workflow.sh
    ├── healthcheck.py
    ├── CHANGELOG.md
    ├── requirements.txt
    └── output.log
└── tarefa-08-projeto-final
    ├── README.md
    ├── collector.py
    ├── processor.py
    ├── run-pipeline.py
    ├── config.yaml
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── run-pipeline.sh
    ├── output
    ├── logs
    └── docs
```

## Progresso

| Tarefa | Status | Descrição |
| --- | --- | --- |
| 01 | Concluída | Coletor de usuários da API JSONPlaceholder |
| 02 | Concluída | Processamento de métricas de servidores |
| 03 | Concluída | Monitor de URLs com retry e logging |
| 04 | Concluída | Containerização do monitor |
| 05 | Concluída | Cliente autenticado para GitHub API |
| 06 | Concluída | Classificador de alertas com Pydantic |
| 07 | Concluída | Workflow Git automatizado |
| 08 | Concluída | Projeto integrado final |

## Observações sobre o desenvolvimento

As soluções foram feitas com foco em clareza, organização e facilidade de execução. Preferi separar cada tarefa em uma pasta própria para deixar o projeto mais simples de revisar.

Também mantive READMEs individuais para explicar como executar cada script e qual foi a ideia usada na implementação.

## Fontes e referências

- API JSONPlaceholder: https://jsonplaceholder.typicode.com
- API ip-api.com: https://ip-api.com/docs/api:json
- Documentação Python: https://docs.python.org/3/
- Guia PEP 8: https://peps.python.org/pep-0008/

## Como executar

Entre na pasta da tarefa desejada e siga as instruções do README local.
