FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-kaz \
    tesseract-ocr-rus \
    libtesseract-dev \
    poppler-utils \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install pipenv daphne --no-cache-dir

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --clear

COPY ./extract ./extract
COPY ./settings ./settings
COPY ./manage.py ./manage.py

RUN addgroup --system appgroup && adduser --system --group appuser \
    && chown -R appuser:appgroup /app

USER appuser

LABEL org.opencontainers.image.source=https://github.com/almazkun/django_image_to_text

ENTRYPOINT ["daphne"]

CMD ["settings.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
