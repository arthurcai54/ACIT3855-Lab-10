from inspect import trace
from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class saleOfItem(Base):
    """ Sale of Item """

    __tablename__ = "sale_item"

    item_id = Column(Integer, primary_key=True)
    product_name = Column(String(250), nullable=False)
    price = Column(Float, nullable=False)
    manufacturer = Column(String(250), nullable=False)
    rating = Column(Integer, nullable=False)
    num_times_bought_before = Column(Integer, nullable=False)
    date_sold = Column(DateTime, nullable=False)
    trace_id = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, item_id, product_name, price, manufacturer, rating, num_times_bought_before, date_sold, trace_id):
        """ Initializes a sale of an item """
        self.item_id = item_id
        self.product_name = product_name
        self.price = price
        self.manufacturer = manufacturer
        self.rating = rating
        self.num_times_bought_before = num_times_bought_before
        self.date_sold = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an item sale reading """
        dict = {}
        dict['item_id'] = self.item_id
        dict['product_name'] = self.product_name
        dict['price'] = self.price
        dict['manufacturer'] = self.manufacturer
        dict['rating'] = self.rating
        dict['num_times_bought_before'] = self.num_times_bought_before
        dict['date_sold'] = self.date_sold
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict
