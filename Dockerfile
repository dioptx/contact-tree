FROM python:3.7.4-alpine3.10

LABEL Name=contactree-app Version=0.0.1

RUN apk add --no-cache build-base gcc

WORKDIR /app
ADD . /app

RUN python3 -m pip install -r requirements.txt

# we have to wait even after wait-for.sh
# because neo4j doesn't work when it starts listening to a port
CMD echo "Waiting for $NEO4J_HOST:$NEO4J_PORT..." && \
    /app/wait-for.sh -t 60 $NEO4J_HOST:$NEO4J_PORT && \
    sleep 15 && \


CMD python run.py