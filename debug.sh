#!/bin/bash

# Banana Math Puzzle Debug Script

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🍌 Banana Math Puzzle - Debug Information 🧮${NC}"

# Python and Virtual Environment Check
echo -e "\n${GREEN}1. Python Environment:${NC}"
python3 --version
which python3
which pip

# Virtual Environment Check
echo -e "\n${GREEN}2. Virtual Environment:${NC}"
if [ -d "venv" ]; then
    echo "Virtual environment exists"
    source venv/bin/activate
    python --version
    deactivate
else
    echo -e "${RED}Virtual environment not found!${NC}"
fi

# Dependency Check
echo -e "\n${GREEN}3. Dependencies:${NC}"
pip list | grep -E "kivy|numpy|aiohttp"

# Project Structure
echo -e "\n${GREEN}4. Project Structure:${NC}"
tree -L 2 .

# Potential Configuration Issues
echo -e "\n${GREEN}5. Configuration Check:${NC}"
if [ -f ".env" ]; then
    echo ".env file exists"
else
    echo -e "${YELLOW}Warning: .env file not found. Using .env.example${NC}"
fi

# Logging Preparation
echo -e "\n${GREEN}6. Logging Preparation:${NC}"
mkdir -p logs
touch logs/banana_math_puzzle.log

# Run Diagnostics
echo -e "\n${GREEN}7. Running Diagnostics:${NC}"
python3 -m pip check
python3 -m pip list

echo -e "\n${YELLOW}Debug script completed. Please review the output.${NC}"
