import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

app = FastAPI()
loop = asyncio.get_event_loop()
kafka_bootstrap_servers: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic: str = os.environ.get("KAFKA_TOPIC")
kafka_topic2: str = os.environ.get("KAFKA_TOPIC2")

async def take_action(topic, msg):
    to_load = msg.value.decode("utf-8")
    sh = json.loads(to_load)
    print(f"Received message from {topic}: {sh}")

async def consume(consumer, topic):
    try:
        await consumer.start()
    except Exception as e:
        print(e)
        return
    try:
        async for msg in consumer:
            await take_action(topic, msg)
    finally:
        await consumer.stop()

async def main_loop():
    consumer = AIOKafkaConsumer(
        kafka_topic,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
    )
    consumer2 = AIOKafkaConsumer(
        kafka_topic2,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
    )

    await asyncio.gather(
        consume(consumer, kafka_topic),
        consume(consumer2, kafka_topic2),
    )

@app.on_event("startup")
async def main():
    asyncio.create_task(main_loop())
    print("Consumers are Up")

@app.get("/")
async def root():
    return {"Kafka": "Consumer"}
