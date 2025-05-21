# scraper/Dockerfile
FROM python:3.11

RUN pip install uv

WORKDIR /scraper

# Copy scraper and shared code

COPY pyproject.toml ./
RUN uv pip compile --output-file requirements.txt pyproject.toml && \
    uv pip install -r requirements.txt --system


COPY ./scraper /scraper
COPY ./shared /shared



CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
