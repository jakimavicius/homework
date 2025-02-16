FROM python:3.13.2-slim

# Set the working directory in the container to /app
WORKDIR /app

# Upgrade pip and install explicit dependencies
RUN pip install \
    --disable-pip-version-check \
    --root-user-action ignore \
    --no-cache-dir \
    "scrapy>=2.12.0" \
    "grpcio>=1.70.0" \
    "grpcio-tools>=1.70.0"

# Set envvar for grpc parser service address
ENV GRPC_PARSER_ADDRESS="localhost:50051"

# Copy files into the container
COPY . .

# Set default command to run the spider
CMD ["scrapy", "crawl", "books"]
