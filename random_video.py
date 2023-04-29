import queue

import numpy as np

import utils


MIN_INSERTION = 5
MAX_INSERTION = 10
MIN_DURATION = 2
MAX_DURATION = 5


class VideoRandomizer:
    def __init__(self):
        with open('classes.txt', 'r') as f:
            self.cls = f.read().split()[:utils.MAXSIZE]
            self.random_indexing()

            try:
                for cls in self.cls:
                    utils.order_q.put_nowait(cls)
            except queue.Full:
                print(len(utils.order_q.queue))

            # self.mini_insertion()
            self.random_insertion()

    def random_indexing(self):
        np.random.shuffle(self.cls)

    def random_insertion(self):
        num_insertion = np.random.randint(MIN_INSERTION, MAX_INSERTION)
        sleep_arr = np.random.randint(low=MIN_DURATION, high=MAX_DURATION, size=utils.MAXSIZE)

        for i in range(utils.MAXSIZE):
            self.cls.insert(utils.MAXSIZE - i - 1, sleep_arr[i])

    def mini_insertion(self):
        for i in range(len(self.cls)):
            self.cls.insert(len(self.cls)-i, self.mini_delay)

    @property
    def random_delay(self):
        return np.random.randint(1, MAX_DURATION)

    @property
    def mini_delay(self):
        return np.random.rand()


if __name__ == '__main__':
    cls = VideoRandomizer().cls
    while not utils.order_q.empty():
        print(utils.order_q.get())
