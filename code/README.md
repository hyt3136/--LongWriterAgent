# WenBen Engine - Chapter 1 Scaffold

This folder contains the chapter-1 engineering baseline:
- layered package layout
- environment-based settings
- health check entrypoint
- minimal test

## Run (PowerShell)

```powershell
$env:PYTHONPATH = "src"
python -m wenben_engine.app --health-check
```

## Run tests

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -p "test_*.py"
```
