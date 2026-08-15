# Teste Técnico — Desenvolvedor Júnior

**Posição:** Desenvolvedor Júnior — Pipelines de Dados, APIs e Automação  
**Prazo de entrega:** 5 dias corridos  
**Formato:** Prático com entregáveis

---

## Sobre o Projeto

Você estará trabalhando em um **pipeline automatizado de análise e enriquecimento de dados**, que consome múltiplas APIs externas, processa dados estruturados, integra com sistemas de terceiros e gera relatórios consolidados.

**Stack principal:** Python (Pydantic, async, logging), Docker Compose, Bash, Git.

---

## Objetivo

Avaliar habilidades essenciais para contribuir com o projeto:

- ✅ **Python** — classes, type hints, Pydantic, tratamento de erros, logging
- ✅ **APIs REST** — autenticação (Bearer token, API key), rate limiting, retry
- ✅ **Docker** — Dockerfile otimizado, Docker Compose, volumes, segurança
- ✅ **Processamento de dados** — parsing, validação, scoring, exportação multi-formato
- ✅ **Bash scripting** — automação, tratamento de erros, validações
- ✅ **Git** — branches, conventional commits, merge workflow
- ✅ **Documentação técnica** — READMEs, arquitetura, instruções

---

## Estrutura de Entrega

```
seu-nome-teste-tecnico/
├── README.md                  (índice geral com instruções)
├── tarefa-01/
│   ├── README.md
│   ├── collector.py
│   ├── requirements.txt
│   └── output.json            (exemplo)
├── tarefa-02/
│   ├── README.md
│   └── ...
├── tarefa-03/
├── tarefa-04/
├── tarefa-05/
├── tarefa-06/
├── tarefa-07/
└── tarefa-08/
```

Cada tarefa deve conter:

- **README.md** explicando como executar
- **Código fonte** completo
- **requirements.txt** (se aplicável)
- **Exemplos de saída/resultados**

---

## Parte 1 — Fundamentos Python

---

### TAREFA 1: Coletor de API REST ⭐

**Objetivo:** Criar um coletor básico de dados de API REST

**Descrição:** Crie um script Python que:

1. Consuma a API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com/users)
2. Permita filtrar usuários por **cidade** (via parâmetro configurável)
3. Calcule estatísticas:
   - Total de usuários encontrados
   - Lista de empresas dos usuários
4. Salve o resultado em JSON com timestamp no nome do arquivo

**Requisitos técnicos:**

- Use **classes** e **métodos**
- Implemente tratamento de exceções
- Adicione **docstrings** nos métodos
- Código limpo e organizado (**PEP 8**)

**Entregável:**

```
tarefa-01/
├── README.md
├── collector.py
├── requirements.txt
├── config.json                (opcional)
└── output.json                (exemplo de saída)
```

**Exemplo de uso esperado:**

```python
collector = UserCollector(
    api_url='https://jsonplaceholder.typicode.com/users',
    city_filter='South Christy'
)
users = collector.fetch_users()
filtered = collector.filter_by_city(users)
stats = collector.generate_stats(filtered)
collector.save_results(filtered, stats)
```

---

### TAREFA 2: Processamento de Dados ⭐⭐

**Objetivo:** Manipular e transformar dados estruturados

**Descrição:** Você recebeu dados de monitoramento em formato bruto. Crie um script Python que processe esses dados.

**Arquivo de entrada (`input.json`):**

```json
{
    "servers": [
        {
            "id": 1,
            "name": "srv-web-01",
            "metrics": "cpu:45|mem:78|disk:62",
            "timestamp": "2026-02-10T08:00:00Z"
        },
        {
            "id": 2,
            "name": "srv-db-01",
            "metrics": "cpu:82|mem:91|disk:45",
            "timestamp": "2026-02-10T08:00:00Z"
        },
        {
            "id": 3,
            "name": "srv-app-01",
            "metrics": "cpu:34|mem:56|disk:78",
            "timestamp": "2026-02-10T08:00:00Z"
        }
    ]
}
```

**O script deve:**

1. Ler o arquivo JSON
2. Fazer **parse das métricas** (formato: `cpu:45|mem:78|disk:62`)
3. Converter para formato estruturado
4. **Identificar servidores com problemas:**
   - CPU > 80%
   - Memória > 90%
5. Gerar relatório em **JSON** e **CSV**
6. Calcular médias de CPU, memória e disco

**Requisitos técnicos:**

- Use **type hints**
- Crie classe **`MetricsProcessor`**
- Métodos bem definidos para cada operação
- Exportação em múltiplos formatos

**Entregável:**

```
tarefa-02/
├── README.md
├── processor.py
├── input.json
├── requirements.txt
├── output.json                (exemplo)
└── output.csv                 (exemplo)
```

---

### TAREFA 3: Coletor com Retry e Logging ⭐⭐

**Objetivo:** Implementar coletor robusto com boas práticas

**Descrição:** Crie um **monitor de URLs** que seja resiliente a falhas.

**O monitor deve:**

1. Verificar **status HTTP** e **tempo de resposta** de URLs
2. Implementar **retry automático** com **backoff exponencial** (máximo 3 tentativas)
3. Usar **logging estruturado** (não `print()`)
4. Ler configurações de **arquivo YAML**
5. Salvar resultados com timestamp

**Requisitos técnicos:**

- Use a biblioteca **`logging`**
- Implemente backoff exponencial: 1s, 2s, 4s
- Configuração externa (YAML)
- Logs em **arquivo** e **console**
- Tratamento específico para diferentes erros (timeout, DNS, SSL, etc.)

**Arquivo `config.yaml` esperado:**

```yaml
urls:
  - https://jsonplaceholder.typicode.com
  - https://api.github.com
  - https://httpbin.org/status/200

max_retries: 3
timeout: 10
log_level: INFO
```

**Entregável:**

```
tarefa-03/
├── README.md
├── monitor.py
├── config.yaml
├── requirements.txt
└── monitor.log                (exemplo)
```

---

## Parte 2 — Docker, Bash e APIs

---

### TAREFA 4: Containerização do Coletor ⭐⭐

**Objetivo:** Containerizar aplicação Python

**Descrição:** Containerize o **monitor da Tarefa 3** usando Docker.

**Requisitos:**

1. Criar **Dockerfile otimizado**
2. Criar **docker-compose.yml**
3. Usar **volumes** para:
   - Arquivo de configuração
   - Diretório de saída
   - Logs
4. Criar **script `run.sh`** para build e execução
5. **Variáveis de ambiente** para configuração

**Dockerfile deve:**

- Usar imagem base oficial Python
- Ser otimizado (camadas mínimas)
- **Não rodar como root** (criar usuário)
- Incluir apenas arquivos necessários

**Script `run.sh` deve:**

- Fazer build da imagem
- Executar container
- Mostrar logs
- Ter tratamento de erros (`set -e`)

**Entregável:**

```
tarefa-04/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── run.sh
├── monitor.py
├── config.yaml
├── requirements.txt
└── .dockerignore
```

---

### TAREFA 5 (NOVA): Cliente API com Autenticação ⭐⭐⭐

**Objetivo:** Consumir uma API que requer **autenticação Bearer token** — prática essencial para APIs modernas.

**Descrição:** Crie um cliente HTTP genérico autenticado.

**O cliente deve consumir a [GitHub API](https://docs.github.com/en/rest):**

1. Autenticar via `Authorization: Bearer <token>`
2. Método `get_user(username)` — retorna dados do usuário
3. Método `list_repos(username, sort='updated')` — retorna repositórios
4. Método `get_rate_limit()` — retorna limites de rate limit da API

**Requisitos técnicos:**

- Classe `AuthenticatedClient` bem estruturada
- Header `Authorization: Bearer <token>` em toda requisição
- Tratamento de **401** (token inválido) e **403** (rate limit excedido)
- Leitura do token de fora do código:
  - Variável de ambiente `API_TOKEN`
  - Ou arquivo externo `~/.config/token.txt`
- Cache de respostas com TTL configurável (evitar bater na mesma URL repetidamente)
- Métodos GET e POST **genéricos** e reutilizáveis
- Type hints em todos os métodos

**Exemplo de uso esperado:**

```python
client = AuthenticatedClient(
    base_url="https://api.github.com",
    token_env_var="API_TOKEN"
)

user = client.get_user("octocat")
print(f"User: {user['login']}, repos: {user['public_repos']}")

repos = client.list_repos("octocat")
for repo in repos[:5]:
    print(f"  - {repo['name']} ({repo['language']})")

rate = client.get_rate_limit()
print(f"Remaining: {rate['rate']['remaining']}/{rate['rate']['limit']}")
```

**Dica:** Para gerar um token GitHub pessoal, vá em GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic). Marque escopo `public_repo` apenas. Não compartilhe o token — use variável de ambiente.

**Entregável:**

```
tarefa-05/
├── README.md
├── auth_client.py
├── github_client.py           (herda de AuthenticatedClient)
├── requirements.txt
├── config.yaml                (opcional)
└── output.json                (exemplo de saída)
```

---

### TAREFA 6 (NOVA): Classificador de Alertas ⭐⭐⭐

**Objetivo:** Processar alertas estruturados, classificar indicadores e calcular scores de risco.

**Descrição:** Crie um processador de alertas que analise indicadores (hashes, IPs, domínios) contra uma base de conhecimento local e calcule prioridades.

**Arquivo de entrada (`alerts.json`):**

```json
{
    "alerts": [
        {
            "id": "ALT-001",
            "name": "Malware/AgentTesla",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "source_ip": "185.220.101.45",
            "domain": "evil.example.com",
            "confidence": "high",
            "timestamp": "2026-07-22T10:30:00Z"
        },
        {
            "id": "ALT-002",
            "name": "Phishing/Link",
            "sha256": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
            "source_ip": "8.8.8.8",
            "domain": "google.com",
            "confidence": "medium",
            "timestamp": "2026-07-22T10:31:00Z"
        },
        {
            "id": "ALT-003",
            "name": "Ransomware/LockBit",
            "sha256": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
            "source_ip": "45.33.32.156",
            "domain": "malware.test",
            "confidence": "high",
            "timestamp": "2026-07-22T10:32:00Z"
        }
    ]
}
```

**Arquivo de base de conhecimento (`known_iocs.csv`):**

```csv
type,value,reason,severity
hash,e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855,Known malware hash,critical
ip,185.220.101.45,Suspicious node,suspicious
domain,evil.example.com,Known C2,critical
hash,01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b,Known ransomware hash,critical
ip,45.33.32.156,Known scanner,suspicious
```

**O script deve:**

1. Ler o JSON de alertas e o CSV de base de conhecimento
2. Classificar indicadores por **tipo** (hash, IP, domínio)
3. Verificar cada indicador contra a base de conhecimento
4. Calcular **score de risco** por alerta:
   - Hash crítico → +40
   - IP suspeito → +30
   - Domínio crítico → +20
   - Confiança "high" → +10
   - Confiança "medium" → +5
5. Classificar prioridade:
   - **Crítico** (score ≥ 80)
   - **Alto** (score ≥ 50)
   - **Médio** (score ≥ 20)
   - **Baixo** (score < 20)
6. Gerar relatório em **JSON** e **CSV** com:
   - Total de alertas processados
   - Indicadores críticos vs limpos
   - Score agregado por alerta
   - Prioridade final

**Requisitos técnicos:**

- **Enum** para `IndicatorType`, `ConfidenceLevel`, `Priority`
- **Pydantic models** para `Alert`, `Indicator`, `Report`
- Função **pura** de scoring (sem side effects — testável isoladamente)
- Use **dataclasses** ou **Pydantic** para todos os modelos de dados

**Entregável:**

```
tarefa-06/
├── README.md
├── processor.py
├── models.py                  (Pydantic models)
├── alerts.json
├── known_iocs.csv
├── requirements.txt
├── output.json                (exemplo)
└── output.csv                 (exemplo)
```

---

### TAREFA 7 (NOVA): Git Workflow e Automação ⭐⭐

**Objetivo:** Simular o fluxo de trabalho real de desenvolvimento — branches, conventional commits, merge.

**Descrição:** Crie um repositório Git local e execute o fluxo completo de desenvolvimento via script Bash.

**Passos (automatizados via bash):**

1. Inicializar um repositório Git local
2. Criar arquivo inicial `healthcheck.py` com uma função simples de health check HTTP
3. Criar branch `feat/health-check-endpoint`
4. Adicionar classe `HealthChecker` com:
   - Método `check(url)` → retorna `{"status": "ok", "response_time_ms": N}`
   - Método `check(url)` → retorna `{"status": "error", "code": N}` em caso de falha
   - Logging estruturado
5. Fazer **commit** com mensagem no padrão **Conventional Commits**
6. Fazer **merge** para a branch `main`
7. Criar arquivo `CHANGELOG.md` com entrada para a nova feature

**Script bash esperado (`git-workflow.sh`):**

```bash
#!/bin/bash
set -euo pipefail

echo "🔄 Inicializando repositório..."
git init
git checkout -b main

echo "📝 Commit inicial..."
# ...

echo "🌿 Criando branch feat/health-check-endpoint..."
git checkout -b feat/health-check-endpoint

echo "✅ Commitando feature..."
git add healthcheck.py
git commit -m "feat: add HTTP health check endpoint

Add HealthChecker class that performs HTTP GET requests
and returns status with response time measurement.

Closes #1"

echo "🔀 Fazendo merge para main..."
git checkout main
git merge feat/health-check-endpoint

echo "📋 Gerando CHANGELOG..."
# ...

echo "🎯 Workflow concluído!"
git log --oneline --graph --all
```

**Requisitos:**

- Script bash com `set -euo pipefail`
- Mensagens de commit no formato [Conventional Commits](https://www.conventionalcommits.org/)
- Uso de branches: `main` → `feat/...` → merge
- CHANGELOG.md gerado (pode ser manual no script)
- Código do `healthcheck.py` funcional e testável

**Entregável:**

```
tarefa-07/
├── README.md
├── git-workflow.sh
├── healthcheck.py
├── CHANGELOG.md
└── output.log                 (exemplo de execução)
```

---

### TAREFA 8 (NOVA): Projeto Integrado Final ⭐⭐⭐⭐

**Objetivo:** Integrar todos os conhecimentos em um **pipeline completo de enriquecimento de dados**.

**Descrição:** Crie um pipeline que coleta dados de uma API pública, enriquece, processa, containeriza e automatiza.

**Componentes:**

#### 1. Coletor Python (`collector.py`)

- Consuma a API pública [ip-api.com](http://ip-api.com/json/{ip}) ou [ipinfo.io](https://ipinfo.io/{ip})
- Enriqueça IPs com: geolocalização, ASN, ISP, organização
- Implemente retry com backoff exponencial (1s, 2s, 4s — máximo 3 tentativas)
- Logging estruturado (arquivo + console)
- Leia lista de IPs de um arquivo YAML

**Arquivo `config.yaml`:**

```yaml
ips:
  - 8.8.8.8
  - 1.1.1.1
  - 185.220.101.45
  - 45.33.32.156

max_retries: 3
timeout: 10
log_level: INFO
output_dir: ./output
```

#### 2. Processador (`processor.py`)

- Leia o JSON de saída do coletor
- Classifique cada IP:
  - **Conhecido legítimo** (Google DNS, Cloudflare, etc.)
  - **Potencialmente suspeito** (datacenter conhecido por abuso, nós de saída)
  - **Desconhecido**
- Gere relatório final em JSON

#### 3. Containerização

- **Dockerfile** multi-stage otimizado
- **docker-compose.yml** com:
  - Volume para dados de entrada
  - Volume para dados de saída
  - Volume para logs
- **Usuário não-root**
- **Health check**

#### 4. Automação Bash (`run-pipeline.sh`)

```bash
#!/bin/bash
set -euo pipefail

# Usage: ./run-pipeline.sh [--input config.yaml] [--output ./results]

usage() {
    echo "Uso: $0 [--input config.yaml] [--output ./results]"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input) CONFIG="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        *) usage ;;
    esac
done

: "${CONFIG:=config.yaml}"
: "${OUTPUT:=./results}"

echo "🔍 Verificando dependências..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker não encontrado"; exit 1; }

echo "🏗️  Buildando imagem..."
docker build -t ip-enricher:latest .

echo "🚀 Executando pipeline..."
docker run --rm \
    -v "$(pwd)/$CONFIG:/app/config.yaml:ro" \
    -v "$(pwd)/$OUTPUT:/app/output" \
    ip-enricher:latest

echo "✅ Pipeline concluído! Resultados em: $OUTPUT"
```

#### 5. Documentação

- **ARCHITECTURE.md** — Diagrama da arquitetura (pode ser ASCII, Mermaid ou texto)
- **SETUP.md** — Como configurar e executar
- **USAGE.md** — Exemplos de uso

**Estrutura esperada:**

```
projeto-final/
├── README.md
├── collector.py
├── processor.py
├── config.yaml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── run-pipeline.sh
└── docs/
    ├── ARCHITECTURE.md
    ├── SETUP.md
    └── USAGE.md
```

---

## O Que Será Avaliado

### Código Python (35%)

| Critério | Peso |
|----------|:----:|
| ✅ Organização e estrutura | 10% |
| ✅ Boas práticas (PEP 8, type hints, docstrings) | 10% |
| ✅ Tratamento de erros | 5% |
| ✅ Uso adequado de bibliotecas | 5% |
| ✅ Pydantic / models bem definidos (Tarefas 6 e 8) | 5% |

### APIs e Integração (25%)

| Critério | Peso |
|----------|:----:|
| ✅ Consumo de API REST com autenticação | 10% |
| ✅ Tratamento de rate limit e erros HTTP | 5% |
| ✅ Retry com backoff exponencial | 5% |
| ✅ Logging estruturado | 5% |

### Docker (20%)

| Critério | Peso |
|----------|:----:|
| ✅ Dockerfile otimizado (multi-stage) | 5% |
| ✅ Docker Compose funcional | 5% |
| ✅ Uso correto de volumes e redes | 5% |
| ✅ Segurança (não rodar como root, health checks) | 5% |

### Bash Scripts (10%)

| Critério | Peso |
|----------|:----:|
| ✅ Scripts robustos com `set -euo pipefail` | 3% |
| ✅ Validações de entrada | 3% |
| ✅ Mensagens claras e informativas | 2% |
| ✅ Uso de funções | 2% |

### Git e Documentação (10%)

| Critério | Peso |
|----------|:----:|
| ✅ Conventional Commits | 3% |
| ✅ READMEs claros em cada tarefa | 3% |
| ✅ Instruções de execução | 2% |
| ✅ Exemplos de saída | 2% |

---

## Níveis de Aprovação

| Nível | Tarefas Completas | Perfil |
|-------|-------------------|--------|
| **Mínimo** | 1, 2, 3, 4 | Consegue manter scripts e pipelines existentes, entende Docker |
| **Bom** | + 5, 6 | Consegue contribuir com consumo de APIs e processamento de dados |
| **Excelente** | + 7 | Consegue trabalhar no fluxo Git do time sem supervisão |
| **Destaque** | + 8 | Consegue pegar uma tarefa completa do zero e entregar |

---

## Dicas Importantes

### ✅ Faça:

- Commit frequentemente no Git com mensagens claras
- Teste tudo antes de entregar
- Documente suas decisões técnicas
- Use `.gitignore` adequado
- Inclua `requirements.txt` em projetos Python
- Escreva READMEs claros em cada tarefa
- Se travar em algo, **documente o que tentou**

### ❌ Evite:

- Hardcoded de credenciais (use variáveis de ambiente)
- Código sem tratamento de erros
- Commits com mensagens genéricas ("update", "fix")
- Dockerfiles com camadas desnecessárias
- Scripts bash sem validações (`set -e`)
- Falta de documentação

---

## Recursos Permitidos

Você pode consultar:

- ✅ Documentação oficial (Python, Docker, Git, GitHub API)
- ✅ Stack Overflow
- ✅ GitHub
- ✅ Tutoriais e artigos técnicos
- ✅ ChatGPT e outras IAs (**documente o uso**)

**Importante:** Documente suas fontes de pesquisa no README principal.

---

## Como Entregar

### Opção 1: Repositório Git

1. Crie um repositório público no GitHub (ou outro provedor git)
2. Envie o link do repositório

### Opção 2: Arquivo Compactado

1. Comprima todo o projeto em `.zip` ou `.tar.gz`
2. Envie via email ou link de download

### O que incluir:

- ✅ Todo o código fonte
- ✅ Arquivos de configuração
- ✅ Documentação
- ✅ Exemplos de saída
- ✅ README.md principal com índice de todas as tarefas

---

## Perguntas de Filtragem Rápida (para entrevista)

1. **"O que é um Bearer token e como você o usaria em uma requisição HTTP?"**
   - _Filtra se entende autenticação de APIs_

2. **"Como você debugaria uma API que retorna 401 na primeira chamada?"**
   - _Filtra se sabe lidar com autenticação_

3. **"O que é backoff exponencial e por que usamos em pipelines de coleta?"**
   - _Filtra se entende resiliência e rate limiting_

4. **"Pra que serve um Dockerfile multi-stage?"**
   - _Filtra se entende otimização de imagem_

5. **"Diferença entre `git merge` e `git rebase`?"**
   - _Filtra maturidade em Git_

6. **"O que é Pydantic e pra que serve?"**
   - _Filtra se conhece validação de dados em Python_

---

## Observações Finais

- Este teste avalia **conhecimentos técnicos** e **capacidade de aprendizado**
- As Tarefas 1–4 são obrigatórias (base); 5–8 são diferenciais
- **Qualidade é mais importante que quantidade**
- Mostre seu **raciocínio e processo** de resolução de problemas
- Seja **honesto** sobre dificuldades encontradas

---

**Boa sorte! 🚀**
