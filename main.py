import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import engine, Base, async_session
from app.api.master import api_router
from app.data.user import init_db


app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url = f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://0.0.0.0:8000",
        "http://127.0.0.1:4200",
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix = settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:    
        await init_db(session=session)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
