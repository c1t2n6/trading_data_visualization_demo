from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger

# Lưu database vào thư mục /tmp để đảm bảo quyền ghi trên Render
DB_URL = "sqlite:////tmp/app.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OHLCV(Base):
    __tablename__ = 'ohlcv'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True)
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    timeframe = Column(String(5))

class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(String(255), primary_key=True)
    symbol = Column(String(20), index=True)
    timestamp = Column(DateTime, index=True)
    price = Column(Float)
    amount = Column(Float)
    cost = Column(Float)
    side = Column(String(10))

class Price(Base):
    __tablename__ = 'price'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(25))
    timestamp = Column(DateTime, index=True)
    price = Column(Float)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    #  Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)