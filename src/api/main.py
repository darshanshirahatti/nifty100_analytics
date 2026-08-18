# src/api/main.py

import time
import sqlite3
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

app = FastAPI(
    title="Nifty 100 Analytics Platform API",
    description="Production REST API providing access to financial metrics, cluster assignments, valuations, and portfolio reports.",
    version="1.0.0"
)

# 1. CORS Middleware (Allow all origins for internal use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Request Logging Middleware (Log method, path, and response time)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Method: {request.method} | Path: {request.url.path} | Duration: {process_time:.4f}s | Status: {response.status_code}")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Method: {request.method} | Path: {request.url.path} | Duration: {process_time:.4f}s | Error: {str(e)}")
        raise

# 3. SQLite Connection Function
from src.config import DB_PATH

def get_db_connection():
    """Get SQLite database connection using shared config path."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 4. Import and Include Routers under /api/v1
from src.api.routers import (
    companies, screener, sectors, peers, valuation, portfolio, documents, health
)

app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(screener.router, prefix="/api/v1", tags=["Screener"])
app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])
app.include_router(peers.router, prefix="/api/v1", tags=["Peers"])
app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

@app.get("/")
def root():
    return {"message": "Nifty 100 Analytics API is active. Go to /docs for interactive Swagger UI."}