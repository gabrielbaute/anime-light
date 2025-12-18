import uvicorn
from fastapi import FastAPI
from animelight.api.include_routers import include_routers

version = "0.4.0"

app = FastAPI(tittle="AnimeLight API", version=version)

include_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)