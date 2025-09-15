from redis import Redis
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

app = FastAPI()
redis_client = Redis(host='redis', port=6379, db=0)
