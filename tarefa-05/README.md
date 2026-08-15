# Tarefa 05 - Cliente API com Autenticação

## Objetivo

Criar um cliente HTTP autenticado usando Bearer token para consumir alguns endpoints da GitHub API.

## O que foi implementado

- Classe `AuthenticatedClient` para concentrar a lógica HTTP reutilizável.
- Header `Authorization: Bearer <token>` em todas as requisições.
- Leitura do token por variável de ambiente `API_TOKEN`.
- Leitura alternativa do token pelo arquivo `~/.config/token.txt`.
- Métodos genéricos `get` e `post`.
- Tratamento específico para:
  - `401`: token inválido ou ausente.
  - `403`: rate limit excedido ou acesso negado.
- Cache em memória com TTL configurável.
- Classe `GitHubClient`, herdando de `AuthenticatedClient`.
- Métodos:
  - `get_user(username)`
  - `list_repos(username, sort="updated")`
  - `get_rate_limit()`

## Como configurar o token

No PowerShell:

```powershell
$env:API_TOKEN="seu_token_aqui"
```

Ou crie o arquivo:

```text
C:\Users\SEU_USUARIO\.config\token.txt
```

E coloque apenas o token dentro dele.

Importante: o token não deve ser salvo dentro do código e não deve ser enviado junto com a entrega.

## Como executar

```powershell
cd "C:\programacao\tarefa-05"
python -m pip install -r requirements.txt
python github_client.py --username octocat
```

Se estiver sem token e quiser apenas gerar um exemplo de saída:

```powershell
python github_client.py --demo
```

## Exemplo de uso no código

```python
client = GitHubClient(
    base_url="https://api.github.com",
    token_env_var="API_TOKEN",
)

user = client.get_user("octocat")
repos = client.list_repos("octocat")
rate = client.get_rate_limit()
```

## Como explicar esta tarefa

Nesta tarefa, eu criei um cliente para consumir uma API que exige autenticação. A parte genérica ficou na classe `AuthenticatedClient`, que sabe montar os headers com Bearer token, fazer requisições GET e POST, tratar erros e guardar respostas em cache por alguns minutos.

Depois criei a classe `GitHubClient`, que herda esse comportamento e adiciona métodos mais específicos da GitHub API, como buscar um usuário, listar repositórios e consultar o rate limit.

Eu também deixei o token fora do código, porque credencial não deve ser escrita diretamente no projeto.
