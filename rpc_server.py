#!/usr/bin/env python
import pika
import os
from functools import lru_cache


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ["RABBITMQ_HOST"]))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

@lru_cache(None)
def fibonacci(num: int) -> int:
	if num < 0:
		print("Incorrect input")
		return

	elif num < 2:
		return num

	return fibonacci(num - 1) + fibonacci(num - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fibonacci(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
