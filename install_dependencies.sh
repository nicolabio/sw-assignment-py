#!/bin/bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python 3.9.18
install_python() {
    if ! command_exists python3.9; then
        echo "Installing Python 3.9.18..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python@3.9
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.9 python3.9-venv python3.9-dev
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            echo "Please install Python 3.9.18 manually on Windows from https://www.python.org/downloads/"
            exit 1
        else
            echo "Unsupported operating system"
            exit 1
        fi
    else
        echo "Python 3.9 is already installed"
    fi
}

# Function to install Taskfile
install_taskfile() {
    if ! command_exists task; then
        echo "Installing Taskfile..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install go-task/tap/go-task
        elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
        else
            echo "Unsupported operating system"
            exit 1
        fi
    else
        echo "Taskfile is already installed"
    fi
}

# Function to install pipx
install_pipx() {
    if ! command_exists pipx; then
        echo "Installing pipx..."
        if command_exists pip3; then
            pip3 install --user pipx
            pipx ensurepath
        else
            echo "pip3 not found. Please install pip3 first."
            exit 1
        fi
    else
        echo "pipx is already installed"
    fi
}


# Main installation process
echo "Starting installation process..."

install_python
install_taskfile
install_pipx

echo "Installation complete!"