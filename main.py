from fastapi import FastAPI

from app import apis

app = FastAPI()

@app.get('/')
async def main():
    return {'message': "This is a Simple Twitter Like App"}

app.include_router(apis.router, prefix="/v1")
