#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Uso: $0 [--input config.yaml] [--output ./output]"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --input) CONFIG="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        *) usage ;;
    esac
done

: "${CONFIG:=config.yaml}"
: "${OUTPUT:=./output}"

echo "Verificando dependencias..."
command -v docker >/dev/null 2>&1 || {
    echo "Docker nao encontrado."
    exit 1
}

mkdir -p "$OUTPUT" logs

echo "Buildando imagem..."
docker build -t ip-enricher:latest .

echo "Executando pipeline..."
docker run --rm \
    -v "$(pwd)/$CONFIG:/app/config.yaml:ro" \
    -v "$(pwd)/$OUTPUT:/app/output" \
    -v "$(pwd)/logs:/app/logs" \
    ip-enricher:latest

echo "Pipeline concluido. Resultados em: $OUTPUT"
