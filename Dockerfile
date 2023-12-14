# docker build -t varadharajaan/scaleit:latest --build-arg BUILD_VERSION=2 .
# docker build -t varadharajaan/scaleit:latest --build-arg BUILD_VERSION=2 PORT=your_custom_port .
# docker run -p 8080:8123 varadharajaan/scaleit:latest

# Build Stage
# Set the base image to Python 3.12.0 and create a build stage named "builder"
FROM python:3.12.0 as builder

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app
COPY . /app

RUN pip install flasgger

# Production Stage
# Create a new stage based on a slimmer Python 3.12.0 image for production
FROM python:3.12.0-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the contents of the /app directory from the builder stage to the /app directory in the production stage
COPY --from=builder /app /app

# Install the Python dependencies specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Add a non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Expose the port for external access (default to 8123 if not provided)
ARG PORT=8213
EXPOSE $PORT

LABEL maintainer="varathu09@gmail.com"

# Set a default value for BUILD_VERSION if not provided during build
ARG BUILD_VERSION=LATEST
LABEL build_version=$BUILD_VERSION

# Set the build date label in EST format
LABEL build_date="$(TZ=America/New_York date +'%Y-%m-%dT%H:%M:%S%z')"

COPY entrypoint.sh /app/entrypoint.sh
USER root
RUN chmod +x /app/entrypoint.sh
USER myuser

# Set the entrypoint script as the main command to run when the container launches
ENTRYPOINT ["/app/entrypoint.sh"]