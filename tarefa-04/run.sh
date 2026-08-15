#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="url-monitor:latest"
SERVICE_NAME="url-monitor"

echo "Verificando Docker..."
command -v docker >/dev/null 2>&1 || {
    echo "Docker nao encontrado. Instale o Docker Desktop e tente novamente."
    exit 1
}

echo "Criando diretorios locais..."
mkdir -p output logs

echo "Buildando imagem..."
docker compose build

echo "Executando container..."
docker compose up --abort-on-container-exit

echo "Mostrando logs do servico..."
docker compose logs "${SERVICE_NAME}"

echo "Workflow finalizado para a imagem ${IMAGE_NAME}."
