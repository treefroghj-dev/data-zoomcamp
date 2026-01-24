FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest_data.py .
# COPY ingest_zone_data.py .

ENTRYPOINT ["python", "ingest_data.py"]
# ENTRYPOINT ["python", "ingest_zone_data.py"]
