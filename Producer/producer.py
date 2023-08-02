import json
import os
from random import choice

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI


app = FastAPI()
kafka_bootstrap_servers: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic: str = os.environ.get("KAFKA_TOPIC")
kafka_topic2: str = os.environ.get("KAFKA_TOPIC2")
superheros = ["Batman", "Spiderman", "Ironman", "Superman", "Aquaman", "Woderwoman", "Hulk"]


def kafka_serializer(value):
    return json.dumps(value).encode()


async def produce(topic: str, msg: str):
    try:
        producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
        await producer.start()
        try:
            await producer.send_and_wait(topic, kafka_serializer(msg))
        finally:
            await producer.stop()
    except Exception as err:
        print(f"Some Kafka error: {err}")


@app.get("/")
async def root():
    return {"Kafka": "Producer"}


@app.get("/start")
async def start():
    sh = choice(superheros)
    sh2 = choice(superheros)
    await produce(topic=kafka_topic, msg=sh)
    await produce(topic=kafka_topic2, msg=sh2)
    return {"Superhero1": sh, "Superhero2": sh2}
