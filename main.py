from src.routers import intent_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.logger import logger

app = FastAPI(title="GAM.DCI ALITAA API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intent_router.router)


@app.on_event("startup")
async def startup_db_client():
    logger.info("App started !!! Welcome to world!")


@app.get("/")
async def root():
    return {"message": "Alitaa"}
