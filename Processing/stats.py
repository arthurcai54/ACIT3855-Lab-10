from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime

class SaleOfItemStats(Base):
    """ Processing Statistics """
    __tablename__ = "max_stats"
    
    id = Column(Integer, primary_key=True)
    highest_price = Column(Float, nullable=False)
    maximum_rating = Column(Integer, nullable=False)
    max_num_items_sold = Column(Integer, nullable=False)
    max_num_times_bought_before = Column(Integer, nullable=False)
    max_num_vans_needed = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    

    def __init__(self, highest_price, maximum_rating, max_num_items_sold, max_num_times_bought_before, max_num_vans_needed, last_updated):
        """ Initializes a processing statistics objet """
        self.highest_price = highest_price
        self.maximum_rating = maximum_rating
        self.max_num_items_sold = max_num_items_sold
        self.max_num_times_bought_before = max_num_times_bought_before
        self.max_num_vans_needed = max_num_vans_needed
        self.last_updated = last_updated

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['highest_price'] = self.highest_price
        dict['maximum_rating'] = self.maximum_rating
        dict['max_num_items_sold'] = self.max_num_items_sold
        dict['max_num_times_bought_before'] = self.max_num_times_bought_before
        dict['max_num_vans_needed'] = self.max_num_vans_needed
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")
        
        return dict
