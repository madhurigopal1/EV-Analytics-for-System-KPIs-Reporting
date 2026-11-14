import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from .analytics import get_engine, summary, segment_kpis, product_kpis
from .data_pipeline import generate_and_load

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("GENERATE_ON_START", "false").lower() == "true":
        # MySQL is declared healthy by compose before this service starts.
        generate_and_load(int(os.getenv("SYNTHETIC_SEED", "42")))
    yield

app = FastAPI(title="EV Analytics Data & Insights", version="1.0.0", lifespan=lifespan)

class GenerateRequest(BaseModel):
    seed: int = Field(default=42, ge=0, le=2_147_483_647)

@app.get("/health")
def health():
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

@app.get("/analytics/summary")
def get_summary():
    return summary()

@app.get("/analytics/segments")
def get_segments():
    return segment_kpis()

@app.get("/analytics/products")
def get_products():
    return product_kpis()

@app.post("/admin/generate")
def generate(request: GenerateRequest = GenerateRequest()):
    try:
        return generate_and_load(request.seed)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Dataset generation failed") from exc
