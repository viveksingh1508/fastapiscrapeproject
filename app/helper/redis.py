import json
import redis.asyncio as redis
from itsdangerous import Signer


import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
SESSION_SECRET = os.getenv("SESSION_SECRET")
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME")
SESSION_TTL = os.getenv("SESSION_TTL")


singer = Signer(SESSION_SECRET)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def get_session_data(session_id: str):
    data = await redis_client.get(f"session:{session_id}")
    return json.loads(data) if data else None


async def set_session_data(session_id: str, data: dict):
    await redis_client.setex(f"session:{session_id}", SESSION_TTL, json.dumps(data))


async def clear_session(session_id: str):
    await redis_client.delete(f"session:{session_id}")


def sign_session_id(session_id: str):
    return singer.sign(session_id.encode()).decode()


def unsign_session_id(signed_id: str):
    try:
        return singer.unsign(signed_id).decode()
    except Exception:
        return None
