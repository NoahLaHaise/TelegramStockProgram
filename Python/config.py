from pathlib import Path

# Gets the directory where the Python script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
CSV_FILE_PATH = SCRIPT_DIR.parent / "CSV_Files"