import os
import time
from my_decorator import schedule_task
import schedule

if __name__ == '__main__':

    @schedule_task("17:57", "day")
    def job():
        os.system('pytest -vs -m live_streaming')


    while True:
        schedule.run_pending()
        time.sleep(1)
