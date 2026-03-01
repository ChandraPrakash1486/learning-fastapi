from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data"
STUDENTS_MARKS_FILE = DATA_DIR / "students_marks.json"
STUDENTS_FILE = DATA_DIR / "students_info.json"
