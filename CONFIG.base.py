### Flask settings
PORT = 9001
DEBUG = False

### MongoDB settings
MONGO_PORT = 33291

MONGO_PW = "password#"
MONGO_USER = "username#"
MONGO_URL = "mongodb://{}:{}@ds133291.mlab.com:33291/classdata".format(MONGO_USER, MONGO_PW)
