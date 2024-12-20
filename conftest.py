# conftest.py
import sys
from pathlib import Path

# Добавляем папку src в PYTHONPATH
sys.path.append(str(Path(__file__).parent / "src"))