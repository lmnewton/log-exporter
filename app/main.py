from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/logs/{file_name}")
async def read_log(file_name: str, search_term: Union[str, None] = None, n: int = -1):
    try:
        with open(f"/var/log/{file_name}", "r") as log_file:
            return f"I found {file_name}"
    except FileNotFoundError:
        return "File does not exist."
