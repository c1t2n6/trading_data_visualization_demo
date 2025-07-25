import ccxt
import pandas as pd
from app.database import get_db, OHLCV, Trade, Price
import time
from app.config import EXCHANGE, TIMEFRAME, SYMBOL, GAP
from datetime import datetime, timedelta, timezone
import app.analyzer as analyzer

def fetch_ohlcv(upd: bool):
    db = next(get_db())
    if (upd == False): 
        period = datetime.now(timezone.utc) - timedelta(days=7)
    else: 
        period = datetime.now(timezone.utc) - timedelta(minutes=GAP)        
    since = int(period.timestamp() * 1000)
    until = int(datetime.now(timezone.utc).timestamp()) * 1000
    try: 
        ohlcv = EXCHANGE.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, since = since, params={'until': until})
        for candle in ohlcv:
            ts = datetime.fromisoformat(EXCHANGE.iso8601(candle[0]).replace("Z", "+00:00"))
            record = OHLCV(
                symbol = SYMBOL,
                timestamp = ts,
                open = candle[1],
                high = candle[2],
                low = candle[3],
                close = candle[4],
                volume = candle[5], 
                timeframe = TIMEFRAME
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy OHLCV: {e}")
    finally:
        pass

def fetch_trades(upd: bool):
    db = next(get_db())
    try:
        if (upd == False): 
            period = datetime.now(timezone.utc) - timedelta(hours=1)
        else: 
            period = datetime.now(timezone.utc) - timedelta(minutes=GAP)        
        since = int(period.timestamp() * 1000)
        until = int(datetime.now(timezone.utc).timestamp()) * 1000
        trades = EXCHANGE.fetch_trades(SYMBOL, since = since, params={'until': until})
        
        for trade in trades:
            record = Trade(
                trade_id = trade['id'],
                symbol = SYMBOL,
                timestamp = datetime.fromisoformat(EXCHANGE.iso8601(trade['timestamp']).replace("Z", "+00:00")),
                price = trade['price'],
                amount = trade['amount'],
                cost = trade['cost'],
                side = trade['side']
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy trade history: {e}")
    finally:
        pass


def fetch_price(upd: bool):
    db = next(get_db())
    try:
        ohlcv = EXCHANGE.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
        print(f"Fetched {len(ohlcv)} candles for {SYMBOL}")
        now_utc = datetime.now(timezone.utc)
        for candle in ohlcv:
            ts = datetime.fromisoformat(EXCHANGE.iso8601(candle[0]).replace("Z", "+00:00"))
            print(f"Candle timestamp: {ts}, Now: {now_utc}")
            if ts > now_utc:
                print(f"Skip future candle: {ts}")
                continue
            # Kiểm tra đã có timestamp này trong DB chưa
            if db.query(Price).filter(Price.timestamp == ts).first():
                continue  # Đã có rồi, bỏ qua
            high = candle[2]
            low = candle[3]
            record = Price(
                symbol = SYMBOL,
                timestamp = ts,
                price = (high + low) / 2
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy Price: {e}")
    finally:
        pass


def crawler_main(ok: bool):
    fetch_ohlcv(0)
    fetch_trades(0)
    fetch_price(0)
    print("Hello")
    while True:
        fetch_ohlcv(1)
        fetch_trades(1)
        fetch_price(1)
        if ok == 1:  
            analyzer.plot_price()
        print(f"Dữ liệu cập nhất lúc {datetime.now(timezone.utc)}")
        time.sleep(GAP * 60)

if __name__ == "__main__":
    crawler_main(1)

