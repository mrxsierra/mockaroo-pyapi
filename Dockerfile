# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12

# Use a specific uv version tag for better reproducibility
FROM ghcr.io/astral-sh/uv:debian-slim AS base

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed
# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python
# Prepend venv and tool bin to PATH for immediate use
ENV PATH="/app/.venv/bin:/root/.local/bin:${PATH}"

# Install Python before the project for caching
RUN uv python install ${PYTHON_VERSION}

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# --- Development Stage ---
FROM base AS dev
WORKDIR /app

# Copy only project definition files initially for efficient caching
COPY pyproject.toml uv.lock* ./

# Install development dependencies using cache mounts
RUN --mount=type=cache,id=uv-cache-dev-${PYTHON_VERSION},target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen

# Copy the rest of the application code
COPY . .

# Create a non-root user for development (best practice for isolation)
ARG DEV_UID=1000
ARG DEV_GID=1000
RUN groupadd --gid ${DEV_GID} devuser && \
    useradd --uid ${DEV_UID} --gid ${DEV_GID} --create-home devuser
USER devuser

# Default command to keep the development container running
CMD ["tail", "-f", "/dev/null"]
