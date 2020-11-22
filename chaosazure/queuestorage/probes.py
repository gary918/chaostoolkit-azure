import os
from chaoslib import Configuration, Secrets
from azure.storage.queue import QueueServiceClient, QueueClient
from logzero import logger


# Can only count 32 visible messages in max
def count_visible_messages(secrets: Secrets = None, queue_name=None) -> int:
    logger.debug(
        f"Start count_visible_messages: queue_name='{queue_name}'")

    queue_client = QueueClient.from_connection_string(
        secrets["connection_string"], queue_name)
    # Peek at messages in the queue
    peeked_messages = queue_client.peek_messages(max_messages=32)

    count = 0
    for peeked_message in peeked_messages:
        count = count+1

    logger.debug(f"{count} messages in the queue:{queue_name}")

    return count
