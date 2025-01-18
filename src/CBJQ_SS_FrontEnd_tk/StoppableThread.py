import threading
import ctypes


# 定义函数，用于向线程抛出异常
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread id")
    elif res != 1:
        # 如果res不为1，说明有多个线程受到了影响，需要重置异常
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# 自定义线程类，添加强制终止功能
class StoppableThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = threading.Event()  # 用于优雅停止线程

    # 这个函数可以直接结束线程
    def raise_exception(self):
        _async_raise(self.ident, SystemExit)

    def stop(self):
        self._stop_event.set()

    def terminate_thread(self):
        self.stop()
        # self.raise_exception()
        if self.is_alive() == 0:
            print("Failed to terminate thread.")
            return 1
        else:
            print("Thread terminated successfully.")
            return 0