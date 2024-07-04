import os
from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from .utils import fileutils

app = FastAPI()

log_dir = os.getenv("LOG_LOCATION", "/var/log")

@app.get("/", include_in_schema=False)
def swagger_redirect():
    response = RedirectResponse(url='/docs')
    return response

@app.get("/logs/{file_name}")
def read_log(file_name: str, search_term: Union[str, None] = None, n: int = -1):
    try:
        return StreamingResponse(fileutils.parse_file(f"{log_dir}/{file_name}", n, search_term), media_type="application/text")
    except FileNotFoundError:
        return "File does not exist."
