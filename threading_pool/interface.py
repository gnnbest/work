
# 接口编程

class Task:
    def run(self):
        # 目的：要求子类必须实现该方法
        raise NotImplementedError



class Pool:

    def add_task(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError