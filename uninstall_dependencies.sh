#!/bin/bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to uninstall Python 3.9.18
uninstall_python() {
    if command_exists python3.9; then
        echo "Uninstalling Python 3.9.18..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew uninstall python@3.9
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get remove --purge -y python3.9 python3.9-venv python3.9-dev
            sudo add-apt-repository --remove -y ppa:deadsnakes/ppa
            sudo apt-get update
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            echo "Please uninstall Python 3.9.18 manually on Windows from the Control Panel."
            exit 1
        else
            echo "Unsupported operating system"
            exit 1
        fi
    else
        echo "Python 3.9 is not installed"
    fi
}

# Function to uninstall Taskfile
uninstall_taskfile() {
    if command_exists task; then
        echo "Uninstalling Taskfile..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew uninstall go-task/tap/go-task
        elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            rm -f /usr/local/bin/task
        else
            echo "Unsupported operating system"
            exit 1
        fi
    else
        echo "Taskfile is not installed"
    fi
}

# Function to uninstall pipx
uninstall_pipx() {
    if command_exists pipx; then
        echo "Uninstalling pipx..."
        pipx uninstall-all
        pip3 uninstall --user pipx
    else
        echo "pipx is not installed"
    fi
}

# Function to uninstall Poetry
uninstall_poetry() {
    if command_exists poetry; then
        echo "Uninstalling Poetry..."
        pipx uninstall poetry
    else
        echo "Poetry is not installed"
    fi
}

# Main uninstallation process
echo "Starting uninstallation process..."

uninstall_python
uninstall_taskfile
uninstall_pipx
uninstall_poetry

echo "Uninstallation complete!"