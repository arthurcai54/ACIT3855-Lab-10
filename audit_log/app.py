import connexion
import swagger_ui_bundle
import yaml
import json
import logging
import logging.config
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def getSellItemInfo(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving sold item at index %d" % index) 

    try: 
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
 
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200

            if msg == consumer[index]:
                return msg, 200

            return {"message": "Event Found"}, 200

    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find sold item at index %d" % index) 
    return { "message": "Not Found"}, 404

def getNumSalesInfo(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received!
     
     
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving sale number at index %d" % index) 

    try: 
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
 
            # Find the event at the index you want and  
            # return code 200 
            # i.e., return event, 200 

            if msg == consumer[index]:
                return msg, 200
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find sale number at index %d" % index) 
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("amazonAPI.yaml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == "__main__":
    app.run(port=8110)