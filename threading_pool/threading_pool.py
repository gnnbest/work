
import threading
import queue
import random
import time
from interface import Task, Pool



class Threading_Pool(Pool):

    ''' 声明一个假任务，当工作线程得到这个任务时，则结束循环
        '''
    class task_Quit(Task):
        def run():
            pass


    def __init__(self, thread_num):

        self.lock_ = threading.Lock()

        self.thread_num_ = thread_num

        self.threadings_ = []

        # queue是自带锁的队列
        self.tasks_ = queue.Queue()

        self.add_task_end_ = False

        for i in range(self.thread_num_):

            t = threading.Thread(target = self.run)
            t.start()
            self.threadings_.append(t)



    def run(self):

        while(True):

            # 此处是先入先出队列（所以 quit task 放在最后）
            task = self.tasks_.get()

            if(isinstance(task, self.task_Quit)):
                break

            else:
                # 如果没有任务会一直等待（此处容易错）
                task.run()



    def add_task(self, cur_task):

        self.tasks_.put(cur_task)



    def close(self):
        # 所有任务放完之后再放置跟线程个数相同的退出任务
        for i in range(len(self.threadings_)):

            self.tasks_.put(self.task_Quit())


        for t in self.threadings_:
            t.join()

        print('all task done !!!!')


