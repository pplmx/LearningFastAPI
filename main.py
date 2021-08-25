import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from router import demo
from utils.logger import get_logger

LOG = get_logger(__name__)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time_ns()
    response = await call_next(request)
    process_time = (time.time_ns() - start_time)/10e6
    response.headers["X-Process-Time"] = str(process_time)
    LOG.debug(f'cost: {process_time}ms')
    return response


app.include_router(demo.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
