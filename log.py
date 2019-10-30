import logging
import time
import os
# import ConfigParser
from logging.handlers import TimedRotatingFileHandler

cuurent_path = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
# config = ConfigParser.ConfigParser()
# config.read(cuurent_path+"/"+'config')
#
# try:
#     if not os.path.exists(config.get('PATHS','log')):
#         os.mkdir(config.get('PATHS','log'))
# except Exception as e:
#     pass


#path = config.get('PATHS','log')+'/'+'tsm.log'
path = "./logs/api.log"

logger = logging.getLogger("API_Log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(funcName)s | %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

handler = TimedRotatingFileHandler(path,when="d",interval=1,backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)


aps_logger = logging.getLogger('apscheduler.scheduler')
aps_logger.addHandler(handler)
aps_logger.addHandler(ch)
aps_logger.setLevel(logging.DEBUG)

# aps_logger = logging.getLogger('apscheduler.executors.default')
# aps_logger.addHandler(handler)
# aps_logger.addHandler(ch)
# aps_logger.setLevel(logging.D)

