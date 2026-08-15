# Uso

## Alterar IPs de entrada

Edite o arquivo `config.yaml`:

```yaml
ips:
  - 8.8.8.8
  - 1.1.1.1
```

Depois execute:

```powershell
python run-pipeline.py
```

## Entendendo a saída

O arquivo `output/final_report.json` mostra:

- Total de IPs analisados.
- Quantos foram classificados como conhecidos legítimos.
- Quantos foram classificados como potencialmente suspeitos.
- Quantos ficaram como desconhecidos.

Cada IP também recebe os dados de país, região, cidade, ISP, organização e ASN.
