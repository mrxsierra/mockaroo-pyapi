# Docker Development Environment

This document describes how to use Docker and Docker Compose for developing this application in a containerized environment.

## Prerequisites

* Docker Desktop installed and running.
* A `.env` file in the project root containing necessary environment variables (e.g., `MOCKAROO_API_KEY`). See `.env.example` if available.

## Building and Running the Development Container

### Common Commands

1. **Build and Start** (detached mode):

    ```bash
    docker compose up --build -d
    ```

    * `--build`: Rebuilds the image using the `Dockerfile` (e.g., `dev` stage).
    * `-d`: Runs the container in the background.

2. **Access the Container Shell**:

    ```bash
    docker compose exec app bash
    ```

3. **Stop and Remove Containers**:

    ```bash
    docker compose down
    ```

    Add `-v` to also remove anonymous volumes.

4. **Rebuild and Restart**:

    ```bash
    docker compose up --build
    ```

5. **View Logs**:

    ```bash
    docker compose logs -f
    ```

6. **Restart the Container**:

    ```bash
    docker compose restart app
    ```

7. **Check Container Status**:

    ```bash
    docker compose ps
    ```

## Development Workflow

1. **Access the Container Shell**:

    ```bash
    docker compose exec app bash
    ```

    The working directory inside the container is `/app`.

2. **Run the Application**:

    ```bash
    docker compose exec app python main.py
    ```

    *(Replace `main.py` with your script if different.)*

3. **Live Code Reloading**:
    Edit files locally using your IDE. Changes (except ignored files) are synchronized to `/app` in the container. Re-run the application to test updates.

4. **Dependency Changes**:
    If `pyproject.toml` or `uv.lock` is updated:

    ```bash
    docker compose down
    docker compose up --build -d
    ```

5. **Stop the Environment**:

    ```bash
    docker compose down
    ```

## References

* [Docker's Python guide](https://docs.docker.com/language/python/)
* [Docker Compose `watch` documentation](https://docs.docker.com/compose/file-watch/)
* [uv documentation](https://github.com/astral-sh/uv)