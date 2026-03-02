# Contributing to PredictKit

Thank you for your interest! 🎉

## Setup

```bash
git clone https://github.com/sharanabasaveshwar/predictkit.git
cd predictkit
pip install -e ".[dev]"
python -m pytest tests/
```

## How to contribute

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run: `pytest` and `ruff check .`
4. Open a Pull Request

## What we welcome
- Bug fixes
- New protocol drivers (implement `SensorDriver` interface)
- Documentation improvements
- Example projects
