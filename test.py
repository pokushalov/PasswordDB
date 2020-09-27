from mydb import mydb
from loguru import logger

logger.info("Starting app")
dbs = mydb("pwds.sqllite", logger)
dbs.addinfo('1', '2', '3', '4')