import os
from typing import Any, Generator, Union


def parse_file(file_name: str, line_count: int, search_term: Union[str|None] = None, buffer_size: int = 4096) -> Generator[str, Any, None]:
    with open(file_name, 'rb') as file_wrapper:

        # Move the pointer to the end of the file
        file_wrapper.seek(0, os.SEEK_END)
        log_chunk = []
        
        # Keep track of how many lines we've pulled for response
        cumulative_count = 0

        while (current_position := file_wrapper.tell()) != 0 and cumulative_count < line_count:

            # Ensure as we seek that we never attempt to seek to a negative index (top of file 0 is min)
            read_position = max(0, current_position - buffer_size)
            file_wrapper.seek(read_position, os.SEEK_SET)

            # Read data into the byte buffer
            binary_data = file_wrapper.read(buffer_size)

            # Split the data at line breaks
            log_chunk = binary_data.splitlines(True)

            # We remove the last element in case of the read being caught mid-line.
            # We only need to worry about this in the case of reads across multiple buffers.
            if read_position != 0:
                log_chunk.pop(0)

                binary_data = b''.join(log_chunk)

            # Move the file pointer up from current location to the next read location
            file_wrapper.seek(max(0, file_wrapper.tell() - len(binary_data)), os.SEEK_SET)
            while len(log_chunk) > 0:
                
                log_chunk_elem = log_chunk.pop().decode("utf-8")
                if search_term is None or search_term in log_chunk_elem:
                    yield log_chunk_elem
                    cumulative_count += 1
                if cumulative_count >= line_count:
                    return