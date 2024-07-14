# Starts from python:3.10 official docker image
FROM python:3.10

# Copy and install the requirements file before app to avoid reloading unnecessary docker compose layers when code changes
COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Set the working container dir to /app and copy all files to app
WORKDIR /app
COPY . /app

# Expose the port 8080
EXPOSE 8080

# Run the command to start the API server
CMD /py/bin/uvicorn app:app --host 0.0.0.0 --port 8080 --timeout-keep-alive 1200