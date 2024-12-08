#!/bin/bash

# Banana Math Puzzle Run Script

# Set color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Ensure script is run from project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Running setup...${NC}"
    bash setup_venv.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check for environment variables
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file with default configurations...${NC}"
    cp .env.example .env
fi

# Run pre-game checks
echo -e "${YELLOW}Running pre-game system checks...${NC}"
python -m pip list | grep -E "kivy|numpy|aiohttp"

# Launch the game
echo -e "${GREEN}Starting Banana Math Puzzle...${NC}"
python main.py

# Deactivate virtual environment
deactivate

echo -e "${GREEN}Game session completed.${NC}"
