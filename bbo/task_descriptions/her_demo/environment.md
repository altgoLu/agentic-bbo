# Environment

Recommended environment setup:

```bash
uv sync --extra dev
```

Runtime requirements for this task include:

- Python 3.11+
- numpy
- pandas
- scikit-learn
- matplotlib
- the base `agentic-bbo` benchmark package and its standard CLI entrypoints

No task-local Docker workflow is required for this smoke demo because the benchmark ships a bundled CSV asset and a pure-Python mock oracle.
