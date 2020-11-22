import json
import time
from azure.storage.queue import QueueServiceClient, QueueClient

# Read the configuration
with open('config.json') as f:
    config = json.load(f)

connection_string = config["secrets"]["queuestorage"]["connection_string"]
queue_name = config["configuration"]["queue_name"]
queue_service_client = QueueServiceClient.from_connection_string(conn_str=connection_string)
queue_client = QueueClient.from_connection_string(connection_string, queue_name)

""" list_queues = queue_service_client.list_queues()
for queue in list_queues:
    print(queue)

print("\nAdding messages to the queue...")

# Send several messages to the queue
queue_client.send_message(u"First message")
queue_client.send_message(u"Second message")
saved_message = queue_client.send_message(u"Third message")

print("\nPeek at the messages in the queue...")

# Peek at messages in the queue
peeked_messages = queue_client.peek_messages(max_messages=20)

for peeked_message in peeked_messages:
    # Display the message
    print("Peak message: " + peeked_message.content) """

i = 3000
while i > 0:
    properties = queue_client.get_queue_properties()
    count = properties.approximate_message_count
    peeked_messages = queue_client.peek_messages(max_messages=32)
    visible_count = len(peeked_messages)
    print(f"Total message: {str(count)}, Visible message:{visible_count}")
    # print(f"Message count:\r{str(count)}",end="")
    i = i-1
    time.sleep(5)