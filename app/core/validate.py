from pathlib import Path

from fastapi import HTTPException

MISSING_FILE = "File not found."
INVALID_INT_PARAM = (
    "Invalid line count provided. Line count must be a positive integer."
)


def validate(file, line_count):
    if not Path(file).is_file():
        raise HTTPException(status_code=404, detail=MISSING_FILE)
    try:
        int(line_count)
        if line_count < 0:
            raise (ValueError())
    except ValueError:
        raise HTTPException(status_code=400, detail=INVALID_INT_PARAM)
