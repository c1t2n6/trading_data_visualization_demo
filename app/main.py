from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.database import get_db, OHLCV, Price, Trade, Base, engine
from app import crawler
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI()

# Cho phép CORS cho frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

class OHLCVSchema(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str
    class Config:
        from_attributes = True

class PriceSchema(BaseModel):
    timestamp: datetime
    price: float
    class Config:
        from_attributes = True

@app.post("/crawl")
def crawl_data():
    crawler.fetch_ohlcv(0)
    crawler.fetch_trades(0)
    crawler.fetch_price(0)
    return {"message": "Crawl thành công"}

@app.get("/")
def root():
    return FileResponse("app/frontend.html")

@app.get("/ohlcv", response_model=List[OHLCVSchema])
def get_ohlcv():
    db = next(get_db())
    data = db.query(OHLCV).order_by(OHLCV.timestamp.desc()).limit(50).all()
    return data

@app.get("/price", response_model=List[PriceSchema])
def get_price():
    db = next(get_db())
    # Lấy 50 bản ghi mới nhất, sau đó đảo ngược để tăng dần theo thời gian
    data = db.query(Price).order_by(Price.timestamp.desc()).limit(50).all()[::-1]
    return data 