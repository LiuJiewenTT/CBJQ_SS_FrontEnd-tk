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
    def raise_exception(self):
        _async_raise(self.ident, SystemExit)

    # 使用 ctypes 终止线程
    def terminate_thread(self):
        thread_id = ctypes.c_long(self.ident)
        res = ctypes.windll.kernel32.TerminateThread(thread_id, 0)
        if res == 0:
            print("Failed to terminate thread.")
            return 1
        else:
            print("Thread terminated successfully.")
            return 0