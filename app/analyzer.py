import matplotlib.pyplot as plt
import pandas as pd
from app.database import get_db, Price
from app.config import SYMBOL, EXCHANGE
from datetime import datetime, timezone

def plot_price():
    db = next(get_db())
    try:
        start_date = datetime(2025, 7, 6, 0, 0, 0, 0)
        end_date = datetime(2025, 7, 9, 0, 0, 0, 0)
        query = db.query(Price).filter(Price.timestamp.between(start_date, end_date)).order_by(Price.timestamp)
        df = pd.read_sql(query.statement, db.bind)
        plt.figure(figsize=(14, 7))
        plt.plot(df['timestamp'], df['price'], label = 'Giá trung bình')
        plt.xlabel('Time')
        plt.ylabel('ASTO/USDT')
        plt.grid()

        plt.show()
        plt.savefig("/app/output/plot.png")
    except Exception as e:
        print(f"Lỗi vẽ biểu đồ {e}")
    finally:
        pass

# plot_price()  # Bỏ tự động chạy khi import module