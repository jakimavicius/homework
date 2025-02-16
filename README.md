# Homework Task: SE

## Overview
Software Engineer homework task including Bonus Development Task.

## Requirements
- Python 3.13.2
- Tested only Linux
- [uv](https://docs.astral.sh/uv/)
- [docker](https://docs.docker.com/engine/)
- [minikube](https://minikube.sigs.k8s.io/docs/)

## Install

```shell
uv python install 3.13.2
uv sync
```

## Running localy
First run the gRPC server that parses raw HTML of book pages.
```
cd server/
uv run python server.py
```

In another terminal tab or window run scrapy spider.
```
cd app/
uv run scrapy crawl books
```

This will start the spider using hard-coded start URL for scraping a subset of books from
[Philosophy](https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html) category.

Output is written to `app/output/` using JSON Lines format, by default.
```
uv run scrapy crawl books -s START_URL=https://books.toscrape.com   # will scrape all books
uv run scrapy crawl books -o output/books.json                      # will output JSON format
```

When done remember to stop gRPC server, running inside the first terminal. Ctrl+C works.

## Running using Docker
Build the parsing server image:
```
cd server/
docker build --tag server .

docker run -p 50051:50051 server:latest
```

Build the scraping app image, in another terminal:
```
cd app/
docker build -t app .
docker run --rm --net=host app

mkdir /tmp/books-output
docker run --net=host --mount type=bind,src=/tmp/books-output,dst=/app/output app:latest
```
Output files will be in `/tmp/books-output` directory.

When done stop the parsing server. Ctrl+C.

## Running using Docker Compose
First build and run the gRPC server:
```
docker-compose up --detach grpc-server
```
Then build the scraping app client:
```
mkdir /tmp/books-output  # this directory gets bound as an output direcotry for the app
docker-compose up grpc-client
```
Once all books of default category are scraped, the client will exit. It can be run again.

Output files will be in `/tmp/books-output` directory.

When done stop the gRPC server:
```
docker-compose down
```

## Running using minikube
Start the `minikube` cluster.
```
minikube start
```

Load Docker images into `minikube` (see above for details)
```
minikube image load server:latest
minikube image load app:latest
```

Deploy parsing server to `minikube`:
```
minikube kubectl -- apply -f kubernetes-server-deployment.yaml
# kuectl apply -f kubernetes-server-deployment.yaml
```

Create a cron job of running scraper app:
```
minikube kubectl -- apply -f kubernetes-app-cronjob.yaml
# kubectl apply -f kubernetes-app-cronjob.yaml
```
This cron job will run scraper every ten minutes. If waiting is boring, submit a job manually:
```
minikube kubectl -- apply -f kubernetes-app-job.yaml
```

Checkout Kubernetes dashboard for `minikube` to see if server deployment went smooth and if job logs contain scraped books data:
```
minikube dashboard
```

Alternatively inspect kubernetes workloads via CLI:
```
kubectl get deployments
kubectl get cronjobs
kubectl get jobs
kubectl get pods
```

When done, bring everythin down via dashboard UI, or manualy:
```
kubectl delete -n default job app
kubectl delete -n default cronjob app-cronjob
kubectl delete -n default deployment grpc-server
```

Stop `minikube`:
```
minikube stop
# minikube delete --all
```
