from platform import python_branch
import connexion
from connexion import NoContent

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from base import Base
from sale_item import saleOfItem
from num_sales import numSales
import yaml
import swagger_ui_bundle
from datetime import datetime
import logging
import logging.config
import uuid
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info(f'Connecting to DB, Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')

DB_ENGINE = create_engine('mysql+pymysql://root:Mahomeboy#15@127.0.0.1:3306/events')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def sellItem(body):
    """ Receives a sale of item reading """

    session = DB_SESSION()

    sale_of_item = saleOfItem(body['item_id'],
                    body['product_name'],
                    body['price'],
                    body['manufacturer'],
                    body['rating'],
                    body['num_times_bought_before'],
                    body['date_sold'],
                    body['trace_id'],
                    body['date_created'])

    session.add(sale_of_item)

    session.commit()
    session.close()

    logger.info("Stored event sellItem reqeuest with a trace id of " + body['trace_id'])

    return "Item sold", 201


def sales(body):
    """ Receives a number of sales reading """

    session = DB_SESSION()

    num_sales = numSales(body['sale_id'],
                body['profits'],
                body['num_items_sold'],
                body['num_vans_needed'],
                body['average_rating'],
                body['trace_id'],
                body['date_created'])

    session.add(num_sales)

    session.commit()
    session.close()

    logger.info("Stored event numSales reqeuest with a trace id of " + body['trace_id'])

    return f"{body['profits']:.2f} made", 201

def getSellItemInfo(start_timestamp, end_timestamp):
    """ Gets the readings of an item sold after the timestamp """

    session = DB_SESSION()

    start_timestamp_datetime = datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    end_timestamp_datetime = datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(saleOfItem).filter(
        saleOfItem.date_created >= start_timestamp_datetime,
        saleOfItem.date_created < end_timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for sold item readings after %s returns %d results" % (start_timestamp, len(results_list)))
    
    return results_list, 200

def getNumSalesInfo(start_timestamp, end_timestamp):
    """ Gets the readings of the number of sales after the timestamp """

    session = DB_SESSION()
    
    start_timestamp_datetime = datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    end_timestamp_datetime = datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(numSales).filter(
        numSales.date_created >= start_timestamp_datetime,
        numSales.date_created < end_timestamp_datetime)
    
    results_list = []
    
    for reading in readings:
        results_list.append(reading.to_dict())
    
    session.close()

    logger.info("Query for number of sales readings after %s returns %d results" % (start_timestamp, len(results_list)))
    
    return results_list, 200

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
 
        if msg["type"] == "sale_item": # Change this to your event type 
            # Store the event1 (i.e., the payload) to the DB
            sellItem(payload) 
        elif msg["type"] == "num_sales": # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB
            sales(payload) 
 
        # Commit the new message as being read 
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("amazonAPI.yaml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8090)
    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start()
