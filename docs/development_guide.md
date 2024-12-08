# Banana Math Puzzle - Development Guide

## Setup and Installation

### Prerequisites
- Python 3.9+
- Virtual Environment
- pip

### Installation Steps
1. Clone the repository
2. Create virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment
   ```bash
   cp src/game/core/.env.example .env
   # Edit .env with your specific configurations
   ```
5. Run tests
   ```bash
   pytest tests/
   ```
6. Start the application
   ```bash
   python3 main.py
   ```

## Development Workflow

### Code Structure
- `src/`: Main application code
  - `game/core/`: Core logic and main modules
  - `game/utils/`: Utility functions and helpers
  - `game/models/`: Data models and schemas
  - `game/screens/`: Game screens and UI logic
- `tests/`: Test suites
  - `unit/`: Unit tests
  - `integration/`: Integration tests
- `docs/`: Project documentation
- `scripts/`: Development utilities

### Testing
- Unit Tests: `pytest tests/unit`
- Integration Tests: `pytest tests/integration`
- Coverage Report: `pytest --cov=src`

### Error Handling
- Use `@handle_exceptions` decorator
- Provide context in exceptions
- Log comprehensive error information

### Logging
- Use `structlog` for structured logging
- Include context in log messages
- Use appropriate log levels

## Best Practices
- Follow PEP 8 guidelines
- Write comprehensive docstrings
- Add type hints
- 100% test coverage goal
- Secure coding practices

## Configuration Management
- Use `.env` for environment-specific settings
- Never commit sensitive information
- Use `config.py` for centralized configuration

## Contribution Guidelines
1. Fork the repository
2. Create feature branch
3. Write tests
4. Implement feature
5. Ensure all tests pass
6. Submit pull request

## Performance Optimization
- Profile code regularly
- Use caching mechanisms
- Minimize external dependencies
- Optimize database queries

## Security Considerations
- Never commit secrets
- Use environment variables
- Validate and sanitize inputs
- Keep dependencies updated

## Troubleshooting
- Check logs in `logs/` directory
- Use verbose mode for debugging
- Consult documentation before opening issues

## Release Process
1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Tag release in git
4. Build and publish package
