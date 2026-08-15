FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY collector.py processor.py run-pipeline.py config.yaml ./

RUN mkdir -p /app/output /app/logs \
    && chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import pathlib; raise SystemExit(0 if pathlib.Path('/app').exists() else 1)"

CMD ["python", "run-pipeline.py", "--config", "config.yaml"]
