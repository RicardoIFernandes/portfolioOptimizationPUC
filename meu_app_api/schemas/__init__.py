from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CommentSchema(BaseModel):
    """ Defines how a new comment should be represented
    """
    stock_id: int = 1
    text: str = "Very promising stock!"


class StockSchema(BaseModel):
    """ Defines how a new stock should be represented
    """
    symbol: str = "AAPL"
    quantity: int = 100
    price: float = 150.50


class StockSearchSchema(BaseModel):
    """ Defines how a stock search should be represented
    """
    symbol: str = "AAPL"


class ListStocksSchema(BaseModel):
    """ Defines how a list of stocks should be represented
    """
    stocks: List[StockSchema]


class CommentViewSchema(BaseModel):
    """ Defines how a comment should be returned
    """
    id: int = 1
    text: str = "Very promising stock!"
    date: datetime = datetime.now()


class StockViewSchema(BaseModel):
    """ Defines how a stock should be returned
    """
    id: int = 1
    symbol: str = "AAPL"
    quantity: int = 100
    price: float = 150.50
    total_value: float = 15050.00
    date_added: datetime = datetime.now()
    comments: List[CommentViewSchema]


class StockDelSchema(BaseModel):
    """ Defines how a stock deletion message should be returned
    """
    message: str
    symbol: str


class ErrorSchema(BaseModel):
    """ Defines how an error message should be returned
    """
    message: str


def present_stock(stock) -> dict:
    """ Returns a representation of a stock following the StockViewSchema
    """
    return {
        "id": stock.id,
        "symbol": stock.symbol,
        "quantity": stock.quantity,
        "price": stock.price,
        "total_value": stock.total_value,
        "date_added": stock.date_added,
        "comments": [{"id": c.id, "text": c.text, "date": c.date} for c in stock.comments]
    }


def present_stocks(stocks) -> dict:
    """ Returns a representation of a list of stocks
    """
    result = []
    for stock in stocks:
        result.append({
            "id": stock.id,
            "symbol": stock.symbol,
            "quantity": stock.quantity,
            "price": stock.price,
            "total_value": stock.total_value,
            "date_added": stock.date_added,
            "comments": [{"id": c.id, "text": c.text, "date": c.date} for c in stock.comments]
        })

    return {"stocks": result}
