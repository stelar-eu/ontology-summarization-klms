FROM python:3.12-slim

# Install build tools required for compiling Python packages like py-stringcompare
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the application code
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh

# Set the entrypoint
ENTRYPOINT ["./run.sh"]
