FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CONFIG_PATH=/app/config.yaml \
    APP_HOME=/app

WORKDIR ${APP_HOME}

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY monitor.py .
COPY config.yaml .

RUN mkdir -p /app/output /app/logs \
    && chown -R appuser:appgroup /app

USER appuser

CMD ["python", "monitor.py"]
