import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] : %(message)s')

list_of_files = [
    "src/_init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb",
]
for filepath in list_of_files:
    file_path = Path(filepath)
    file_dir = file_path.parent
    if not file_dir.exists():
        logging.info(f"Creating directory: {file_dir}")
        file_dir.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        logging.info(f"Creating file: {file_path}")
        file_path.touch()
    