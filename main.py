from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def main():
    return {'message': "This is a Simple Twitter Like App"}
    