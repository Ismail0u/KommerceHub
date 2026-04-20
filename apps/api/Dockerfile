FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Development ─────────────────────────────
FROM base AS development

COPY requirements/base.txt requirements/local.txt ./requirements/
RUN pip install -r requirements/local.txt

COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ── Production ──────────────────────────────
FROM base AS production

COPY requirements/base.txt ./requirements/
RUN pip install -r requirements/base.txt

RUN groupadd --gid 1001 django && \
    useradd --uid 1001 --gid django --shell /bin/bash --create-home django

COPY --chown=django:django . .
USER django
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]