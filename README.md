# Python App with MinIO using Docker Compose

This project sets up a Python application with MinIO using Docker Compose. The Python application uses Poetry for dependency management.

## Prerequisites

- Docker
- Docker Compose
- Make

## Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a `pyproject.toml` file in the `app` directory for your Python application dependencies. For example:

    ```toml
    [tool.poetry]
    name = "python_app"
    version = "0.1.0"
    description = ""
    authors = ["Your Name <you@example.com>"]

    [tool.poetry.dependencies]
    python = "^3.9"
    minio = "^7.1.0"

    [tool.poetry.dev-dependencies]
    pytest = "^7.0"
    pytest-mock = "^3.6.1"
    ```

3. Create a `poetry.lock` file by running:

    ```sh
    cd app
    poetry lock
    cd ..
    ```

4. Install dependencies:

    ```sh
    make install
    ```

## Usage

### Start the services
