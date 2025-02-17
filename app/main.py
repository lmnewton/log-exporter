import os
from typing import Union

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.params import Query, Path
from fastapi.responses import JSONResponse, RedirectResponse
from .core import parser
from .core.logging import logger, startup_log
from .core.validate import validate
from .core.constants import READ_LOCATION, BUFFER_SIZE, READ_DEFAULT, BUFFER_DEFAULT
from fastapi_pagination import Page, add_pagination, paginate

log_dir = os.getenv(READ_LOCATION, READ_DEFAULT)
buffer = int(os.getenv(BUFFER_SIZE, BUFFER_DEFAULT))

app = FastAPI(
    title="LogExporter",
    description="Server-based API for searching and retrieving selective log data.",
    on_startup=[startup_log],
)

@app.get("/", include_in_schema=False)
def swagger_redirect():
    logger.info("Redirecting to Swagger UI from root.")
    response = RedirectResponse(url="/docs")
    return response


@app.get(
    "/logs/{file_name:path}",
    description="Invokes the log parser based on how many lines need to be read and which search terms are sought.\n\n**Note:** If both a line limit and the search term are defined, only the top n (where n is the line number) will be returned, even if there are more hits in the file.",
    response_model=Page,
)
def read_log(
    file_name: str = Path(
        ...,
        description=f"The name of a file on disk read from the {log_dir} directory.",
    ),
    lines_to_read: int = Query(
        ...,
        description="If a search term is specified, this parameter indicates that the first n hits starting from the bottom of the file and searching upwards will be returned.\n\nIf no search term is provided, this parameter determines how many lines will be returned from the bottom of the file upwards.",
    ),
    search_term: Union[str, None] = Query(
        None,
        description="A search term to match against. Defaults to none.",
    ),
) -> Page[str]:
    """Invokes the log parser based on how many lines need to be read and which search terms are sought.

    Args:
        file_name (str): The name of the file to be pulled from disk.
        lines_to_read (int): The number of lines from the bottom of the file to read.
        search_term (Union[str, None], optional): The search term to match against. Defaults to None.

    Returns:
        Response: Returns a paged response from the server.
    """

    if search_term is not None:
        suffix = f" matching term '{search_term}'"
    else:
        suffix = ""

    logger.info(
        f"Reading log {log_dir}/{file_name}. Returning last {lines_to_read} lines{suffix}."
    )

    file = f"{log_dir}/{file_name}"

    validate(file, lines_to_read)

    return paginate(
        parser.parse_file(file, lines_to_read, search_term, buffer_size=buffer)
    )


# Overwriting the validation handler response to be consistent with other error handling throughout the application.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, _exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid parameter provided. Check input."}
        ),
    )


add_pagination(app)
