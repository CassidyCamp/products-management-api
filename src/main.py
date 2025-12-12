from fastapi import FastAPI
from .moduls import *
from .db import engine, Base
from .routers import category, product



app = FastAPI()


app.include_router(category.router, prefix='/categories')
app.include_router(product.router, prefix='/product')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)