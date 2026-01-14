from fastapi import FastAPI
from routes import router
import uvicorn

from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="Service B")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)

