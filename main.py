import time

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis.asyncio.connection import ConnectionPool

from src.api.routers.dishes import router as router_dishes
from src.api.routers.menus import router as router_menus
from src.api.routers.submenus import router as router_submenus

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World!'}


@app.post('/clear')
async def clear():
    return await FastAPICache.clear(namespace='test')


@app.get('/test')
@cache(namespace='test', expire=100)
async def test():
    time.sleep(2)
    return 'cache'


@app.on_event('startup')
async def startup():
    pool = ConnectionPool.from_url(url='redis://redis')
    r = redis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(r), prefix='fastapi-cache')


app.include_router(router_menus)
app.include_router(router_submenus)
app.include_router(router_dishes)
