FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY knowledge ./knowledge
COPY agents ./agents
COPY .opencode ./.opencode
COPY skills ./skills
COPY precompiled-binaries ./precompiled-binaries
RUN mkdir -p /app/data

EXPOSE 8000
CMD ["redops", "serve", "--host", "0.0.0.0", "--port", "8000"]
