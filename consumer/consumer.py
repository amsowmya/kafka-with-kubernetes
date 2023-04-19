from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)

class Consumer:
    def __init__(self):
        self.__init__kafka_consumer()

    def __init__kafka_consumer(self):
        self.kafka_host="kafka-ss-0-0.kafka-0.default.svc.cluster.local:30092"
        self.kafka_topic="my-topic"
        self.consumer=KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_host
        )

    def consume_from_kafka(self):
        for message in self.consumer:
            logging.info(message.value)

if __name__ == "__main__":
    consumer = Consumer()
    while True:
        consumer.consume_from_kafka()