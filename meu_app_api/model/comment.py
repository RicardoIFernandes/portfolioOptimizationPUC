from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column("pk_comment", Integer, primary_key=True)
    text = Column(String(4000))
    date = Column(DateTime, default=datetime.now())
    stock_id = Column(Integer, ForeignKey("stock.pk_stock"), nullable=False)

    def __init__(self, text:str):
        """
        Create a Comment instance

        Arguments:
            text: the comment text
        """
        self.text = text 