#!/bin/bash

# Banana Math Puzzle Virtual Environment Setup Script

# Set color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure script is run from project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${YELLOW}Detected Python Version: $PYTHON_VERSION${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install project dependencies
echo -e "${YELLOW}Installing project dependencies...${NC}"
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install the project in editable mode
pip install -e .

# Verify installations
echo -e "${GREEN}✓ Virtual Environment Setup Complete${NC}"
echo -e "${YELLOW}Python Path: $(which python)${NC}"
echo -e "${YELLOW}Python Version: $(python --version)${NC}"

# Optional: Run tests to verify setup
echo -e "${YELLOW}Running project tests...${NC}"
pytest tests/

# Deactivate virtual environment
deactivate

echo -e "${GREEN}Setup completed successfully!${NC}"
