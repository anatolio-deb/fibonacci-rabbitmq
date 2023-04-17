#!/bin/sh

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
    sleep 0.1
done

# proceed to docker command
exec "$@"