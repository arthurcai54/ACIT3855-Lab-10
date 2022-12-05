from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class numSales(Base):
    """ Heart Rate """

    __tablename__ = "num_sales"

    sale_id = Column(Integer, primary_key=True)
    profits = Column(Float, nullable=False)
    num_items_sold = Column(Integer, nullable=False)
    num_vans_needed = Column(Integer, nullable=False)
    average_rating = Column(Float, nullable=False)
    trace_id = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, sale_id, profits, num_items_sold, num_vans_needed, average_rating, trace_id, date_created):
        """ Initializes a number of sales reading """
        self.sale_id = sale_id
        self.profits = profits
        self.num_items_sold = num_items_sold
        self.num_vans_needed = num_vans_needed # Sets the date/time record is created
        self.average_rating = average_rating
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a number of sales reading """
        dict = {}
        dict['sale_id'] = self.sale_id
        dict['profits'] = self.profits
        dict['num_items_sold'] = self.num_items_sold
        dict['num_vans_needed'] = self.num_vans_needed
        dict['average_rating'] = self.average_rating
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created
        
        return dict
