from fastapi import FastAPI
from routers import instagram

app = FastAPI()

app.include_router(router=instagram.router, )
