from fastapi import FastAPI

from app import api

app = FastAPI()

@app.get('/')
async def main():
    return {'message': "This is a Simple Twitter Like App"}

app.include_router(api.router, prefix="/v1")
