import time
import keyboard


def labelling_thread():
    global start_q, stop_q
    start_pressed = False
    stop_pressed = False
    start_time = time.perf_counter()

    while True:
        if keyboard.is_pressed('a') and not start_pressed:
            start_pressed = True
            time_ = time.perf_counter() - start_time
            start_q.put(time_)
        elif not keyboard.is_pressed('a') and start_pressed:
            start_pressed = False

        if keyboard.is_pressed('b') and not stop_pressed:
            stop_pressed = True
            time_ = time.perf_counter() - start_time
            stop_q.put(time_)
        elif not keyboard.is_pressed('b') and stop_pressed:
            stop_pressed = False

        elif keyboard.is_pressed('q'):
            print('Shutting down')
            break

# def labelling_thread(start_q, stop_q):
#     start_pressed = False
#     stop_pressed = False
#     start_time = time.perf_counter()
#
#     while True:
#         if keyboard.is_pressed('a') and not start_pressed:
#             start_pressed = True
#             time_ = time.perf_counter() - start_time
#             start_q.put(time_)
#         elif not keyboard.is_pressed('a') and start_pressed:
#             start_pressed = False
#
#         if keyboard.is_pressed('b') and not stop_pressed:
#             stop_pressed = True
#             time_ = time.perf_counter() - start_time
#             stop_q.put(time_)
#         elif not keyboard.is_pressed('b') and stop_pressed:
#             stop_pressed = False
#
#         elif keyboard.is_pressed('q'):
#             print('Shutting down')
#             break


# Test multithreading
def get_q(start_q, stop_q):
    while True:
        print(start_q.get())
        print(stop_q.get())


if __name__ == '__main__':
    from queue import Queue
    from threading import Thread

    start_q = Queue(maxsize=19)
    stop_q = Queue(maxsize=19)

    t1 = Thread(target=labelling_thread, args=(start_q, stop_q))
    t2 = Thread(target=get_q, args=(start_q, stop_q))
    t1.start()
    t2.start()


