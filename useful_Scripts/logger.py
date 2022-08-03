# importing module
import logging

# Create and configure logger
logging.StreamHandler()
#if filename:
# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     filemode='w')

#display console
logging.basicConfig(
                    format='%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger(__name__)

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")