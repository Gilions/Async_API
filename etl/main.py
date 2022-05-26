from time import sleep

from config import TIME_OUT
from utility import UpdateElasticStorage

if __name__ == '__main__':
    while True:
        UpdateElasticStorage().run()
        sleep(TIME_OUT)
