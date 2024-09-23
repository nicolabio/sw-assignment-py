# Use an official Python runtime as the base image
FROM python:3.9.18-bookworm

# Set environment variables
ENV PATH=$PATH:/root/.local/bin

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the entire project
COPY . .

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Run the application
CMD ["python", "-m", "sw_assignment"]