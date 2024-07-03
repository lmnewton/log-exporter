# Log Exporter

A simple REST service for accessing logs within /var/log on the host machine.

## Running the Application in a Container

This app requires docker and docker-compose to run in production mode.

To deploy this project onto a server:
1. Clone the project to the deployment location on the server.
2. Run `docker-compose up`. This will run the initial-build.
    - Note that rebuilding the image after the initial build should be initiated with `docker-compose build` instead.

This will expose the service running on port 8000.

## Running the Application Outside of a Container
1. Clone the project. Initialize a virtual environment.
2. Once running in the context of the virtual environment, install dependencies with `pip install /log-exporter/requirements.txt`.
3. Run `fastapi dev main.py`.

This will expose the service running locally on port 8000.

## Development Considerations
- Caution around user input.
- How do we handle ordering in the case of asynchronous file growth?
- How should we handle memory constraints?
- Consider edge cases (missing file, corrupt file, empty file, etc).
- Consider how to communicate details of response (e.g. empty set of hits vs no logs to evaluate)