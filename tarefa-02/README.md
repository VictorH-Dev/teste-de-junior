# Tarefa 02 - Processamento de Dados

## Objetivo

Processar dados brutos de monitoramento de servidores, transformar as metricas em uma estrutura mais organizada, identificar possiveis problemas e gerar relatorios em JSON e CSV.

## O que foi implementado

- Classe `MetricsProcessor` para organizar o fluxo da tarefa.
- Leitura do arquivo `input.json`.
- Parse das metricas no formato `cpu:45|mem:78|disk:62`.
- Conversao para um formato estruturado.
- Identificacao de servidores com:
  - CPU acima de 80%.
  - Memoria acima de 90%.
- Calculo das medias de CPU, memoria e disco.
- Exportacao do relatorio em `output.json` e `output.csv`.

## Decisoes tecnicas

Usei apenas bibliotecas nativas do Python porque a tarefa nao exige dependencias externas. Isso deixa o exercicio mais simples de executar e mais facil de revisar.

Separei o codigo em metodos pequenos para cada etapa: ler dados, converter metricas, identificar problemas, calcular medias e exportar os arquivos. Essa separacao ajuda a testar e entender cada parte sem misturar tudo em uma unica funcao.

## Como executar

No PowerShell:

```powershell
cd "C:\programacao\tarefa-02"
python processor.py
```

Tambem e possivel informar os arquivos manualmente:

```powershell
python processor.py --input input.json --json-output output.json --csv-output output.csv
```

## Exemplo de saida no terminal

```text
Processamento concluido.
Total de servidores: 3
Servidores com problemas: 1
Arquivo JSON: output.json
Arquivo CSV: output.csv
```

## Como explicar esta tarefa

Nesta tarefa, eu recebo metricas de servidores em um formato bruto, separo os valores de CPU, memoria e disco, transformo esses dados em campos estruturados e verifico se algum servidor passou dos limites definidos. Depois gero um relatorio em JSON, mais completo, e um CSV, que facilita abrir os dados em planilhas.
