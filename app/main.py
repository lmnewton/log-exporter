import os
from typing import Union


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .utils import fileutils
from .core.logging import logger
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI(
    title="LogExporter",
    description="Server-based API for searching and retrieving selective log data.",
)
add_pagination(app)

log_dir = os.getenv("LOG_LOCATION", "/var/log")
buffer = int(os.getenv("BUFFER_SIZE", 4096))


@app.get("/", include_in_schema=False)
def swagger_redirect():
    logger.info("Redirecting to Swagger UI from root.")
    response = RedirectResponse(url="/docs")
    return response


@app.get(
    "/logs/{file_name}",
    description="Invokes the log parser based on how many lines need to be read and which search terms are sought.",
)
def read_log(
    file_name: str, lines_to_read: int, search_term: Union[str, None] = None
) -> Page[str]:

    """Invokes the log parser based on how many lines need to be read and which search terms are sought.

    Args:
        file_name (str): The name of the file to be pulled from disk.
        lines_to_read (int): The number of lines from the bottom of the file to read.
        search_term (Union[str, None], optional): The search term to match against. Defaults to None.

    Returns:
        Response: Returns a response from the server.
    """

    logger.info(
        f"Reading log {log_dir}/{file_name}. Returning last {lines_to_read} lines and retrieving term '{search_term}'."
    )

    return paginate(
        fileutils.parse_file(
            f"{log_dir}/{file_name}", lines_to_read, search_term, buffer_size=buffer
        )
    )
