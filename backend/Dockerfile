# This Dockerfile is used to build an image for a Django application.

# We are using the python:3.12.1-alpine image as our base image.
# Alpine Linux is much smaller than most distribution base images (~5MB),
# which leads to much slimmer images in general.
FROM python:3.12.1-alpine AS builder

# Installs the bash shell in the Docker image.
# The 'apk add' command is used to install packages in Alpine Linux.
# The '--no-cache' option tells apk to skip the cache, which reduces the size of the image.
RUN apk add --no-cache bash

# This Dockerfile exposes port 8000 to the network.
# This is the default port for Django's development server.
EXPOSE 8000
# Sets the working directory in the Docker image to /app.
# All subsequent commands will be run from this directory.
WORKDIR /app

# Copy entrypoint script and set execution permission
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copies the base.txt file from your Docker client's current directory to /app in the Docker image.
COPY config/requirements/base.txt /app
COPY config/requirements/dev.txt /app

# Installs the Python dependencies that are listed in the base.txt file.
# The --no-cache-dir option tells pip to disable its cache, which reduces the size of the image.
RUN pip install --upgrade pip
RUN pip install -r dev.txt --no-cache-dir

# Copies everything from your Docker client's current directory to /app in the Docker image.
COPY . /app