# Tarefa 06 - Classificador de Alertas

## Objetivo

Processar alertas de segurança, extrair indicadores como hash, IP e domínio, comparar esses indicadores com uma base local de conhecimento e calcular uma prioridade final para cada alerta.

## O que foi implementado

- Leitura do arquivo `alerts.json`.
- Leitura da base `known_iocs.csv`.
- Classificação de indicadores por tipo:
  - hash
  - ip
  - domain
- Validação dos dados usando Pydantic.
- Uso de `Enum` para tipos, confiança, severidade e prioridade.
- Função pura `calculate_risk_score`, que calcula o score sem alterar arquivos ou depender de estado externo.
- Geração de relatório em JSON e CSV.

## Como o score funciona

Cada alerta começa com score zero. Depois o sistema soma pontos conforme os indicadores encontrados:

```text
Hash crítico      +40
IP suspeito       +30
Domínio crítico   +20
Confiança high    +10
Confiança medium  +5
```

Depois do score calculado, a prioridade é definida assim:

```text
80 ou mais = Crítico
50 ou mais = Alto
20 ou mais = Médio
menos de 20 = Baixo
```

## Como executar

No PowerShell:

```powershell
cd "C:\programacao\tarefa-06"
python -m pip install -r requirements.txt
python processor.py
```

## Exemplo de saída no terminal

```text
Processamento de alertas concluido.
Total de alertas: 3
Indicadores criticos: 3
Indicadores limpos: 4
Arquivo JSON: output.json
Arquivo CSV: output.csv
```

## Como explicar esta tarefa

Nesta tarefa, eu criei um classificador de alertas. O sistema lê alertas em JSON, pega os indicadores principais de cada alerta, como hash, IP e domínio, e compara esses valores com uma base local em CSV.

Se algum indicador aparece na base, o sistema marca esse indicador como conhecido e usa a severidade dele no cálculo de risco. Depois, cada alerta recebe um score e uma prioridade final.

Eu separei os modelos em `models.py` usando Pydantic para validar melhor os dados, e deixei a regra de pontuação em uma função separada para facilitar teste e entendimento.
