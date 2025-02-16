FROM python:3.13.2-slim

# Set the working directory in the container to /app
WORKDIR /app

# Upgrade pip and install explicit dependencies
RUN pip install \
    --disable-pip-version-check \
    --root-user-action ignore \
    --no-cache-dir \
    "grpcio>=1.70.0" \
    "grpcio-tools>=1.70.0" \
    "parsel>=1.10.0"

# Copy the project files into the container
COPY . .

EXPOSE 50051

# Set default command to run the spider
CMD ["python", "server.py"]
