FROM python:3.11 as python


RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    dos2unix \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install gunicorn
RUN pip install gunicorn

# Copy requirements.txt before copying the rest of the code for better caching
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/backend
COPY ./docker /app/docker

# Make sure the entrypoint scripts are executable
RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/beat-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh

# Set the entrypoint to one of your scripts as an example
# Change this according to your needs
ENTRYPOINT ["/app/docker/backend/server-entrypoint.sh"]

