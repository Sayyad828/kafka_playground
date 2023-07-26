import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

app = FastAPI()
loop = asyncio.get_event_loop()
kafka_bootstrap_servers: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic: str = os.environ.get("KAFKA_TOPIC")

async def take_action(msg):
    to_load = msg.value.decode("utf-8")
    sh = json.loads(to_load)
    print(f"The best superhero is: {sh}")


async def consume():
    consumer = AIOKafkaConsumer(
        kafka_topic,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
    )

    try:
        await consumer.start()

    except Exception as e:
        print(e)
        return
   
    try:
        async for msg in consumer:
            await take_action(msg)

    finally:
        await consumer.stop()


@app.on_event("startup")
async def main():
    asyncio.create_task(consume())
    print("Consumer is Up")


@app.get("/")
async def root():
    return {"Kafka": "Consumer"}

