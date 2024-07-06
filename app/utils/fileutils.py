import os
from typing import Any, Generator, Union


def parse_file(
    file_name: str,
    line_count: int,
    search_term: Union[str | None] = None,
    buffer_size: int = 4096,
) -> Generator[str, Any, None]:

    """Opens and parses a file object from the bottom up by manipulating the file read pointer.

    Args:
        file_name (str): The full path of the file to be pulled from disk.
        line_count (int): The number of lines from the bottom of the file to read.
        search_term (Union[str  |  None], optional): The search term to match against. . Defaults to None.
        buffer_size (int, optional): The size of the read buffer. Defaults to 4096.

    Yields:
        Generator[str, Any, None]: Generator which yields queried log lines.
    """

    with open(file_name, "rb") as file_wrapper:

        # Keep track of how many lines we've pulled for response
        cumulative_count = 0

        # Move the pointer to the end of the file
        file_wrapper.seek(0, os.SEEK_END)

        # Keep track of mid-line buffer splits to ensure we captire the full lines.
        scrollback = 0

        while current_position := file_wrapper.tell() or scrollback != 0:

            # Ensure we only read in as much as we need when we are on the last buffered read
            read_size = min(buffer_size, current_position)

            # Move the pointer to either the buffer size or the remaining bytes to top of file.
            file_wrapper.seek(-read_size, os.SEEK_CUR)

            # Read data into the byte buffer
            binary_data = file_wrapper.read(read_size)

            # Split the data at line breaks
            log_chunk = binary_data.splitlines(True)

            # If this is not the last read before EOF, we want to pop off a piece to use to size where the cursor should move.
            if current_position - buffer_size > 0:
                scrollback = len(log_chunk.pop(0))
            else:
                scrollback = 0

            # Loop through the chunks and determine if it should be returned or not.
            while len(log_chunk) > 0:
                log_chunk_elem = log_chunk.pop().decode("utf-8")
                if search_term is None or search_term in log_chunk_elem:
                    yield log_chunk_elem
                    cumulative_count += 1

                if cumulative_count >= line_count:
                    return

            # Move the file pointer up from current location to the next read location based on the length we've already read.
            # Add the scrollback to ensure that we are covering the chunks we ignored in this iteration.
            file_wrapper.seek(-len(binary_data) + scrollback, os.SEEK_CUR)
