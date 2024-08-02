from uuid import *
from datetime import *
import time
print(datetime.utcnow())

cookie_value = str(f"{str("uuidd")} , {str(int(time.time()))} , {str(int(time.time())+600)}").split(",")
print(cookie_value)