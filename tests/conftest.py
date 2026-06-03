"""Make the tests/ directory importable so `import _loaders` resolves regardless
of pytest invocation directory."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
