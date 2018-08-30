
import time
from interface import Task
import random
from threading_pool import Threading_Pool


class Sleep_Task(Task):

    def __init__(self, wait_time, num_task):

        self.wait_time_ = wait_time

        self.num_task_ = num_task


    def run(self):

        print('task ' + str(self.num_task_) + ' begin ...')

        time.sleep(self.wait_time_)

        print('task ' + str(self.num_task_) + ' end ...')




if __name__ == '__main__':

    threading_num = 100
    pool = Threading_Pool(threading_num)

    task_num = 50
    for task_num in range(task_num):

        wait_time = random.randint(1, 3)
        cur_task = Sleep_Task(wait_time, task_num)

        pool.add_task(cur_task)

    pool.close()