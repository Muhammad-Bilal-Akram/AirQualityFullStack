from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from utils_f.cache import precompute_metrics
from routers import pm25, hamburg

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pm25.router, prefix="/pm25", tags=["PM2.5"])
app.include_router(hamburg.router, prefix="/hamburg", tags=["Hamburg"])

@app.on_event("startup")
async def startup_event():
    os.makedirs("cache", exist_ok=True)
    precompute_metrics()
    print("Precomputed PM2.5 data on startup")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
