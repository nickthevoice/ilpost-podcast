# An example of using standalone Python builds with multistage images.

# First, build the application in the `/app` directory
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR /python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python before the project for caching
RUN uv python install 3.10.16

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Then, use a final image without uv
FROM debian:bookworm-slim AS PRODUCTION

# Install required packages
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create app user and group
RUN groupadd -r app && useradd -r -g app app

# Copy the Python version
COPY --from=builder /python /python

# Copy the application from the builder
COPY --from=builder /app /app

# Set proper permissions
RUN chown -R app:app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Add cron configuration
COPY crontab /etc/cron.d/cron-job

# Create cron configuration with environment variables first
RUN echo "SHELL=/bin/bash\n\
PATH=/app/.venv/bin:$PATH\n\
WORKDIR=/app\n\
\n\
$(cat /etc/cron.d/cron-job)" > /etc/cron.d/my-cron-job

# Set up logging
RUN touch /var/log/cron.log && \
    chmod 666 /var/log/cron.log && \
    chmod 0644 /etc/cron.d/my-cron-job

# Apply the crontab
RUN crontab /etc/cron.d/my-cron-job

# Create directory for cron PID file
RUN mkdir -p /var/run && \
    chmod 755 /var/run

# Start cron and monitor logs
CMD service cron start && tail -f /var/log/cron.log