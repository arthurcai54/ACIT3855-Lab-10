from platform import python_branch
from urllib import response
import connexion
from connexion import NoContent

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import yaml
import swagger_ui_bundle
from datetime import datetime
import logging
import logging.config
import uuid
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from stats import SaleOfItemStats
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def populate_stats():

    logger.info("Start Periodic Processing")

    session = DB_SESSION()

    latestSaleOfItemStat = session.query(SaleOfItemStats).order_by(SaleOfItemStats.last_updated.desc()).first()

    # query_results = session.execute(latestSaleOfItemStat).fetchall()
    # print(query_results)
    # read timestamp from query result
    
    timestamp = datetime.now()
    timestamp_str = str(timestamp.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S.%f"))
    
    if latestSaleOfItemStat == None:
    # logger.info("Statistics do not exist")
        final_stats = SaleOfItemStats(100.00, 5, 3, 10, 100, timestamp_str)  

    # read all events from the database that have happened since the timestamp

    # GET endpoint 1
    response1 = requests.get("http://localhost:8090/sell?timestamp=" + timestamp_str)

    print("RESPONSE 1" + str(response1))

    response1_json = response1.json()
    print(response1_json)
    # each_purchase = []
    
    # for item in response1_json:
    #     print(type(item))
    #     print(item)
    #     each_purchase.append(float(item['max_num_times_bought_before']))
    
    logger.info(f"Number of events received: {len(response1_json)}")
    if response1.status_code != 200:
        logger.error("No response")

    print("HERE")
    # print("MAX_NUM_TIMES " + latestSaleOfItemStat['max_num_times_bought_before'])

    max_num_times_bought = max(0, final_stats.max_num_times_bought_before)

    print(max_num_times_bought)

    logger.debug("Updated statistics for maximum number of times bought before: " + str(max_num_times_bought))

    # GET endpoint 2
    response2 = requests.get("http://localhost:8090/numsales?timestamp=" + timestamp_str)

    print("RESPONSE 2" + str(response2))

    response2_json = response2.json()

    logger.info(f"Number of events received: {len(response2_json)}")

    if response1.status_code != 200:
        logger.error("No response")
    
    max_num_vans = max(0, final_stats.max_num_vans_needed)

    logger.debug("Updated statistics for maximum number vans needed: " + str(max_num_vans))

    final_stats = SaleOfItemStats(final_stats.highest_price,
                            final_stats.maximum_rating,
                            final_stats.max_num_items_sold,
                            final_stats.max_num_times_bought_before,
                            final_stats.max_num_vans_needed,
                            final_stats.last_updated)

    session.add(final_stats)
    logger.info("End Periodic Processing")
    session.commit()
    session.close()

def get_stats():
    
    stats_dict = {}

    logger.info("Start Periodic Processing")
    
    session = DB_SESSION()

    results = session.query(SaleOfItemStats).order_by(SaleOfItemStats.last_updated.desc())

    query_results = session.execute(results).fetchall()

    current_stats = query_results[0][0]

    stats_dict = {
        "highest_price": current_stats.highest_price,
        "maximum_rating": current_stats.maximum_rating,
        "max_num_times_bought_before": current_stats.max_num_times_bought_before,
        "max_profit": current_stats.max_profit,
        "max_num_vans_needed": current_stats.max_num_vans_needed
        }

    logger.debug("Contents of stats dictionary" + stats_dict)
    
    logger.info("Request has completed")

    return stats_dict, 200


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("amazonAPI.yaml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
