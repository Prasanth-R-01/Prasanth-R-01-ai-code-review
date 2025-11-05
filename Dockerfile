# Dockerfile
FROM python:3.10-slim


# system deps
RUN apt-get update && apt-get install -y git --no-install-recommends && rm -rf /var/lib/apt/lists/*


WORKDIR /app


# copy only requirements first for better caching (we'll just use pip installs inline)
COPY app/ ./app/
COPY sample_code/ ./sample_code/


RUN pip install --no-cache-dir openai pygithub



ENTRYPOINT ["python", "-m", "app.review"]
