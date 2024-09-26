# Python App with MinIO using Docker Compose

This project sets up a Python application with MinIO using Docker Compose. The Python application uses Poetry for dependency management.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9.18
- Poetry
- Taskfile

## Setup

1. Run the installation script to set up the required dependencies:

    ```sh
    ./install_dependencies.sh
    ```

   This script will install Python 3.9.18, Taskfile, pipx, Poetry, and set up the Poetry environment.

2. Verify the project setup:

    ```sh
    task all
    ```

   This command will run all tasks, including formatting, linting, testing, building the Docker image, and running the Docker Compose setup.

## Project Structure

- `sw_assignment/`: Main Python package
- `tests/`: Test files
- `Dockerfile`: Docker configuration for the Python app
- `docker-compose.yml`: Docker Compose configuration
- `Taskfile.yml`: Task runner configuration
- `pyproject.toml`: Poetry project configuration

## Usage

To run the application:

```sh
task up
```

To view the logs:

```sh
task logs
```

To stop the application:

```sh
task down
```

To run all together:

```sh
task run
```

## Development

- Use `task format` to run all formatters
- Use `task lint` to run all linters
- Use `task test` to run all tests
- Use `task dev` to run the formatters, linters, and tests

For more detailed task information, refer to the `Taskfile.yml`.