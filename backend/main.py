from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import scanner
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nifty 250 Breakout Scanner API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LineData(BaseModel):
    color: str
    data: List[Dict[str, Any]]
    lineWidth: int

class ScanResult(BaseModel):
    symbol: str
    category: str
    patterns: List[str]
    close: float
    change: float
    volume: int
    chart_data: List[Dict[str, Any]]
    entry: float
    target: float
    sl: float
    hold_time: str
    lines: List[LineData]
    conviction: str
    conviction_score: int
    reason: str
    is_top_pick: bool

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/scan", response_model=List[ScanResult])
async def trigger_scan():
    """Trigger a scan across the Nifty 250 stocks."""
    logger.info("Starting scan...")
    try:
        results = scanner.run_scan()
        logger.info(f"Scan complete. Found {len(results)} breakout stocks.")
        return results
    except Exception as e:
        logger.error(f"Error during scan: {e}")
        return []
