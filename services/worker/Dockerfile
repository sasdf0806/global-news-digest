FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY services/worker/requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY services/worker/app ./app
COPY packages ./packages

CMD ["celery", "-A", "app.celery_app", "worker", "--loglevel=INFO"]
