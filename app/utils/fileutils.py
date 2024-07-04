import os


def read_file(file_name: str, line_count: int, buffer_size: int = 4096):
    with open(file_name, 'rb') as file_wrapper:

        # Move the pointer to the end of the file
        file_wrapper.seek(0, os.SEEK_END)
        log_chunk = []
        
        # Keep track of how many lines we've pulled for response
        cumulative_count = 0

        while (position := file_wrapper.tell()) != 0 and cumulative_count < line_count:

            # Ensure as we seek that we never attempt to seek to a negative index (top of file 0 is min)
            file_wrapper.seek(max(0, position - buffer_size), os.SEEK_SET)

            # Read data into the byte buffer
            binary_data = file_wrapper.read(buffer_size)

            # Move the file pointer up from current location to the next read location
            file_wrapper.seek(file_wrapper.tell() - len(binary_data), os.SEEK_SET)

            # Split the data at line breaks
            log_chunk = binary_data.splitlines(True)

            while len(log_chunk) > 0:
                yield log_chunk.pop().decode("utf-8")
                cumulative_count += 1
                if cumulative_count >= line_count:
                    return