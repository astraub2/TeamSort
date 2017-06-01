### Flask settings
PORT = 9001
DEBUG = False

### MongoDB settings
MONGO_PORT = 57487

MONGO_PW = "password#"
MONGO_USER = "username#"
MONGO_URL = "mongodb://{}:{}@ds117821.mlab.com:17821/class-data".format(MONGO_USER, MONGO_PW)
