# Contributing to QuantOps Engine

Thank you for your interest in contributing to QuantOps Engine! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/REDDNoC/quantops-engine.git
   cd quantops-engine
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=quantops tests/

# Run specific test file
pytest tests/unit/test_engine.py

# Run with verbose output
pytest -v
```

## Code Style

We follow PEP 8 guidelines with the following tools:

- **Black** for code formatting (line length: 100)
- **Flake8** for linting
- **MyPy** for type checking (optional but recommended)

```bash
# Format code
black quantops/

# Check linting
flake8 quantops/

# Type checking
mypy quantops/
```

## Project Structure

```
quantops-engine/
├── quantops/           # Main package
│   ├── core/          # Core trading engine
│   ├── exchange/      # Exchange integration
│   ├── backtesting/   # Backtesting framework
│   ├── models/        # AI/ML models
│   ├── strategies/    # Trading strategies
│   ├── api/           # FastAPI REST API
│   ├── config/        # Configuration
│   └── utils/         # Utilities
├── tests/             # Test suite
├── examples/          # Example scripts
└── docs/              # Documentation
```

## Adding New Features

### Adding a New Strategy

1. Create a new file in `quantops/strategies/`
2. Inherit from `BaseStrategy`
3. Implement the `generate_signal` method
4. Add tests in `tests/unit/`

Example:
```python
from quantops.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    async def generate_signal(self, market_data):
        # Your logic here
        return {"action": "buy", "symbol": "BTC/USDT", "amount": 0.1}
```

### Adding New Indicators

1. Add your indicator function to `quantops/utils/indicators.py`
2. Follow the existing pattern (use pandas Series)
3. Add comprehensive tests
4. Update documentation

### Adding API Endpoints

1. Add endpoint to `quantops/api/app.py`
2. Use Pydantic models for request/response validation
3. Add proper error handling
4. Document with FastAPI's automatic OpenAPI

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common setup
- Mock external dependencies (exchanges, databases)
- Test both success and failure cases

## Documentation

- Update README.md for major features
- Add docstrings to all public methods (Google style)
- Include type hints
- Provide examples in docstrings

Example docstring:
```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose
    and behavior in more detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
    pass
```

## Pull Request Process

1. **Fork the repository** and create a new branch
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** following the guidelines above

3. **Write or update tests** for your changes

4. **Run tests and linting** to ensure everything passes
   ```bash
   pytest
   black quantops/
   flake8 quantops/
   ```

5. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add feature: description of feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create a Pull Request** with:
   - Clear title and description
   - Reference any related issues
   - List of changes made
   - Testing performed

## Code Review Process

- All submissions require review
- We may suggest changes or improvements
- Keep your PR focused and minimal
- Be responsive to feedback

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Minimal code example

## Feature Requests

We welcome feature requests! Please:

- Check existing issues first
- Provide clear use case
- Explain expected behavior
- Consider implementation approach

## Questions?

- Open a Discussion on GitHub
- Join our community chat (if available)
- Check existing documentation and examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professionalism

Thank you for contributing to QuantOps Engine!
