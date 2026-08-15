# Tarefa 03 - Coletor com Retry e Logging

## Objetivo

Criar um monitor de URLs mais robusto, capaz de verificar status HTTP, medir tempo de resposta, tentar novamente em caso de falha e registrar logs em arquivo e console.

## O que foi implementado

- Classe `URLMonitor` para organizar o monitoramento.
- Leitura das URLs e configuracoes pelo arquivo `config.yaml`.
- Verificacao de status HTTP e tempo de resposta.
- Retry automatico com backoff exponencial.
- Backoff de 1s, 2s e 4s, conforme o numero de tentativas.
- Logs estruturados em JSON no console e no arquivo `monitor.log`.
- Tratamento separado para timeout, erro SSL, erro de conexao e erro geral de requisicao.
- Resultado salvo em JSON com timestamp no nome.

## Como funciona o retry

Se uma URL falhar, o sistema nao desiste imediatamente. Ele tenta novamente ate o limite definido em `max_retries`.

Entre as tentativas, ele espera um tempo progressivo:

```text
1 tentativa falhou -> espera 1 segundo
2 tentativa falhou -> espera 2 segundos
3 tentativa falhou -> encerra, se o limite for 3
```

Esse comportamento e chamado de backoff exponencial. Ele ajuda a evitar que o sistema fique insistindo muito rapido em uma API que pode estar lenta ou instavel.

## Como executar

No PowerShell:

```powershell
cd "C:\programacao\tarefa-03"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python monitor.py
```

## Exemplo de saida no terminal

```text
Monitoramento concluido.
Total de URLs: 3
Sucesso: 3
Falhas: 0
```

## Arquivos gerados

- `monitor.log`: logs estruturados do monitoramento.
- `monitor_results_YYYYMMDD_HHMMSS.json`: resultado completo da execucao.

## Como explicar esta tarefa

Nesta tarefa, eu criei um monitor de URLs que verifica se algumas APIs estao respondendo. Para cada URL, o sistema mede o tempo de resposta e registra o status HTTP. Se alguma chamada falhar, ele tenta novamente usando uma espera progressiva entre as tentativas. Tambem usei logging em vez de print para registrar melhor o que aconteceu durante a execucao.
