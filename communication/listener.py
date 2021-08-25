import socketio
from fastapi import FastAPI

from utils.logger import get_logger

LOG = get_logger(__name__)

sio = socketio.AsyncServer(async_mode='asgi')


def listener(app: FastAPI):
    socketio.ASGIApp(sio, app)

    @sio.event
    async def connect(sid, data):
        LOG.info(f'Connect with {sid}, {data}')
        await sio.emit('send', 'hello world')

    @sio.event
    async def disconnect(sid):
        LOG.info(f'{sid}')
        await sio.emit('send', 'GoodBye ~')

    @sio.on('message')
    async def message(sid, data):
        LOG.info(f'{sid} {data}')

