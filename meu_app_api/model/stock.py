from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Comment


class Stock(Base):
    __tablename__ = 'stock'

    id = Column("pk_stock", Integer, primary_key=True)
    symbol = Column(String(10), unique=True)
    quantity = Column(Integer)
    price = Column(Float)
    total_value = Column(Float)
    date_added = Column(DateTime, default=datetime.now())

    # Relationship with comments
    comments = relationship("Comment", cascade="all, delete-orphan")

    def __init__(self, symbol:str, quantity:int, price:float):
        """
        Create a Stock instance

        Arguments:
            symbol: stock symbol (e.g., AAPL, GOOGL)
            quantity: number of shares
            price: price per share
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.total_value = quantity * price

    def add_comment(self, comment:Comment):
        """
        Add a comment to the stock
        """
        self.comments.append(comment) 