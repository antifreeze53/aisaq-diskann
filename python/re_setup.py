import shutil
import subprocess
import sys
from pathlib import Path


BASE = Path.home() / "projects" / "aisaq-diskann"
DATA_DIR = BASE / "build" / "data"
SETUP_SCRIPT = Path(__file__).resolve().parent / "setup.py"


def main() -> None:
    if DATA_DIR.exists():
        print(f"removing {DATA_DIR}")
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"re-running {SETUP_SCRIPT}")
    subprocess.run([sys.executable, str(SETUP_SCRIPT)], check=True)


if __name__ == "__main__":
    main()

