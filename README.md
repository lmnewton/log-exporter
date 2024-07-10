# Log Exporter

A simple REST service for accessing logs within /var/log (or configurable) on the host machine.

## Using the API

The API documentation is available through the Swagger UI that can be accessed via http://localhost:8000 (when running locally). Requests can be sent through this UI as well.

Additionally, you can use the `logs` endpoint using curl:
``` bash
curl -X 'GET' \
   'http://localhost:8000/logs/output.log?lines_to_read=40&page=1&size=50' \
   -H 'accept: application/json'
```

## Running the API

### Configuration
This application only has two configurations and both are set with sensible defaults.

| Env Variable      | Description | Default     |
| :---        |    :----   |          ---: |
| READ_LOCATION      | Where on the filesystem the API should be looking for logs       | `/var/logs`   |
| BUFFER_SIZE   | The size of the file chunk to read into memory for processing at a time        | 4096 (bytes) |

### Running in a Container

This app requires docker and docker-compose to run in production mode.

To deploy this project onto a server:
1. Clone the project to the deployment location on the server.
2. Create a .env file to configure the application and put it in the same directory as the docker-compose file (the project root). Below are the recommended defaults:
    ```
    READ_LOCATION="/logs"
    BUFFER_SIZE=8192
    ```
3. Run `docker-compose --env-file .env up`.

This will expose the service running on port 8000. The root endpoint redirects to a Swagger UI which documents the API.

#### Notes about container run mode
- The logs are read across a **read-only** mount to the host filesystem located at the configured location `READ_LOCATION`. If this is not set it will default to `/var/logs` which is not recommended in containerized mode as you will want to keep your container's logs in tact and separate from the host filesystem's logs.
- If the code changes, make sure to run `docker-compose up --build` on start or `docker-compose build` before start. This setup does not auto-refresh and the image must be manually rebuilt.

### Running Outside of a Container
1. Clone the project. Initialize a virtual environment.
2. Once running in the context of the virtual environment, install dependencies with `pip install /log-exporter/requirements.txt`.
3. Run `fastapi dev main.py`.

This will expose the service running locally on port 8000. The root endpoint redirects to a Swagger UI which documents the API.

#### Notes about local run mode
- The default read buffer size is 4096. This can be changed by setting an environment variable locally.
- The logs are read from `/var/logs` on the underlying system.
- If the code changes, the changes will be redeployed automatically as long as the server is still running.

## Known Issues
- The buffer size must be large enough to accomodate the longest line in the log file. The default when running in production mode is 8192 bytes.
- This API is reading from a Linux file system, so *nix-style line endings are expected within the log file.
- This API uses logic that reads from the current location in a file. If the file is being written to at a rate that is far larger than the buffer size, it's possible results could be shifted. However, if lines are added at a reasonable rate to the bottom of the file and the buffer is set to a sufficient size, there should be no issue as besides the initial cursor location setting, the file read cursor is relative to its last location, not to the top or bottom of the file.
- Similarly, if a log is configured to roll over (log.log.1, log.log.2, etc) and rolls over concurrently with read, only the lines remaining in the current file will be read.
