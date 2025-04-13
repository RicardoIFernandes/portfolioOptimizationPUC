from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Stock, Comment
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Stock Portfolio API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# defining tags
home_tag = Tag(name="Documentation", description="Documentation style selection: Swagger, Redoc or RapiDoc")
stock_tag = Tag(name="Stock", description="Add, view and remove stocks from portfolio")
comment_tag = Tag(name="Comment", description="Add comments to stocks in portfolio")


@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi documentation page.
    """
    return redirect('/openapi')


@app.post('/stock', tags=[stock_tag],
          responses={"200": StockViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_stock(form: StockSchema):
    """Add a new stock to the portfolio

    Returns a representation of the stock and associated comments.
    """
    stock = Stock(
        symbol=form.symbol,
        quantity=form.quantity,
        price=form.price)
    logger.debug(f"Adding stock with symbol: '{stock.symbol}'")
    try:
        # creating database connection
        session = Session()
        # adding stock
        session.add(stock)
        # committing the new item to the database
        session.commit()
        logger.debug(f"Added stock with symbol: '{stock.symbol}'")
        return present_stock(stock), 200

    except IntegrityError as e:
        # duplicate symbol is likely the reason for IntegrityError
        error_msg = "Stock with same symbol already exists in portfolio :/"
        logger.warning(f"Error adding stock '{stock.symbol}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # for unexpected errors
        error_msg = "Could not save new stock :/"
        logger.warning(f"Error adding stock '{stock.symbol}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/stocks', tags=[stock_tag],
         responses={"200": ListStocksSchema, "404": ErrorSchema})
def get_stocks():
    """Get all stocks in the portfolio

    Returns a list of all stocks.
    """
    logger.debug(f"Collecting stocks")
    # creating database connection
    session = Session()
    # fetching all stocks
    stocks = session.query(Stock).all()

    if not stocks:
        # if no stocks are found
        return {"stocks": []}, 200
    else:
        logger.debug(f"%d stocks found" % len(stocks))
        # returns the stock representation
        print(stocks)
        return present_stocks(stocks), 200


@app.get('/stock', tags=[stock_tag],
         responses={"200": StockViewSchema, "404": ErrorSchema})
def get_stock(query: StockSearchSchema):
    """Search for a stock by its symbol

    Returns a representation of the stock and associated comments.
    """
    stock_symbol = query.symbol
    logger.debug(f"Collecting data for stock #{stock_symbol}")
    # creating database connection
    session = Session()
    # searching for the stock
    stock = session.query(Stock).filter(Stock.symbol == stock_symbol).first()

    if not stock:
        # if stock is not found
        error_msg = "Stock not found in portfolio :/"
        logger.warning(f"Error searching for stock '{stock_symbol}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Stock found: '{stock.symbol}'")
        # returns the stock representation
        return present_stock(stock), 200


@app.delete('/stock', tags=[stock_tag],
            responses={"200": StockDelSchema, "404": ErrorSchema})
def del_stock(query: StockSearchSchema):
    """Delete a stock from portfolio by its symbol

    Returns a confirmation message.
    """
    stock_symbol = unquote(unquote(query.symbol))
    print(stock_symbol)
    logger.debug(f"Deleting stock #{stock_symbol}")
    # creating database connection
    session = Session()
    # removing the stock
    count = session.query(Stock).filter(Stock.symbol == stock_symbol).delete()
    session.commit()

    if count:
        # returns confirmation message
        logger.debug(f"Deleted stock #{stock_symbol}")
        return {"message": "Stock removed", "symbol": stock_symbol}
    else:
        # if stock is not found
        error_msg = "Stock not found in portfolio :/"
        logger.warning(f"Error deleting stock #'{stock_symbol}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/comment', tags=[comment_tag],
          responses={"200": StockViewSchema, "404": ErrorSchema})
def add_comment(form: CommentSchema):
    """Add a new comment to a stock in the portfolio

    Returns a representation of the stock and associated comments.
    """
    stock_id = form.stock_id
    logger.debug(f"Adding comment to stock #{stock_id}")
    # creating database connection
    session = Session()
    # searching for the stock
    stock = session.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        # if stock is not found
        error_msg = "Stock not found in portfolio :/"
        logger.warning(f"Error adding comment to stock '{stock_id}', {error_msg}")
        return {"message": error_msg}, 404

    # creating the comment
    text = form.text
    comment = Comment(text)

    # adding comment to the stock
    stock.add_comment(comment)
    session.commit()

    logger.debug(f"Added comment to stock #{stock_id}")

    # returns the stock representation
    return present_stock(stock), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
