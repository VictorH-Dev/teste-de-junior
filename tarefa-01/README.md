# Tarefa 01 - Coletor de API REST

## Objetivo

Criar um coletor simples para consumir a API pública JSONPlaceholder, filtrar usuários por cidade, gerar estatísticas e salvar o resultado em JSON.

## O que foi implementado

- Classe `UserCollector` para concentrar a lógica principal.
- Busca de usuários via HTTP GET.
- Filtro configurável por uma ou mais cidades.
- Estatísticas com total geral, empresas encontradas e resumo por cidade.
- Exportação em JSON com timestamp no nome do arquivo.
- Tratamento de erros para falhas HTTP, timeout e resposta inválida.
- Docstrings e type hints para facilitar leitura e manutenção.

## Cidades usadas no filtro

O arquivo `config.json` foi configurado com as cidades:

- Carapicuíba
- São Paulo
- Osasco
- Barueri

Um ponto importante: a JSONPlaceholder é uma API pública de testes e os usuários dela possuem cidades fictícias. Por isso, essas cidades podem retornar zero resultados. Mesmo assim, mantive o filtro com cidades reais para demonstrar que o script aceita uma lista configurável e gera um relatório organizado sem quebrar quando não encontra registros.

## Decisões técnicas

Usei a biblioteca `requests` porque ela deixa a chamada HTTP mais direta e legível para este nível de exercício. Também separei o fluxo em métodos pequenos para que cada parte tenha uma responsabilidade clara: buscar dados, filtrar, gerar estatísticas e salvar o resultado.

O filtro de cidade ignora diferença entre maiúsculas e minúsculas. Isso evita falhas por capitalização, por exemplo `são paulo`, `São Paulo` ou `SÃO PAULO`.

## Como executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute usando o `config.json`:

```bash
python collector.py
```

Ou informe cidades manualmente:

```bash
python collector.py --city "Carapicuíba" --city "São Paulo" --city "Osasco" --city "Barueri"
```

## Exemplo de uso no código

```python
collector = UserCollector(
    api_url="https://jsonplaceholder.typicode.com/users",
    city_filters=["Carapicuíba", "São Paulo", "Osasco", "Barueri"],
)
users = collector.fetch_users()
filtered = collector.filter_by_city(users)
stats = collector.generate_stats(filtered)
collector.save_results(filtered, stats)
```

## Exemplo de saída

O arquivo gerado segue este formato:

```json
{
  "generated_at": "2026-08-12T04:35:00.000000+00:00",
  "city_filters": [
    "Carapicuíba",
    "São Paulo",
    "Osasco",
    "Barueri"
  ],
  "stats": {
    "total_users": 0,
    "companies": [],
    "cities_checked": [
      "Carapicuíba",
      "São Paulo",
      "Osasco",
      "Barueri"
    ],
    "results_by_city": {
      "Carapicuíba": {
        "total_users": 0,
        "companies": []
      },
      "São Paulo": {
        "total_users": 0,
        "companies": []
      },
      "Osasco": {
        "total_users": 0,
        "companies": []
      },
      "Barueri": {
        "total_users": 0,
        "companies": []
      }
    }
  },
  "users": []
}
```

O arquivo `output.json` neste diretório é um exemplo fixo de saída para facilitar a avaliação.
