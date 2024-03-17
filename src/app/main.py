from contextlib import asynccontextmanager

import uvicorn
from db.base import create_db_and_tables, create_users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import base, user


@asynccontextmanager
async def lifespan(app: FastAPI):  # app is required, but not used now
    create_db_and_tables()
    create_users()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base.router)
app.include_router(user.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
