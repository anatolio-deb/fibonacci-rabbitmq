FROM python:latest
RUN pip install pika
RUN apt update && apt install netcat -y
WORKDIR /code
COPY rpc_server.py rpc_server.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672
ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "python",  "rpc_server.py" ]