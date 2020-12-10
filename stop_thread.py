#!/usr/bin/env python3

import threading
import inspect
import ctypes
import time


def say_hello():
    """
    print once a second "Hello, World"
    :return: None
    """
    while True:
        time.sleep(1)
        print('Hello, World')


def _async_raise(thread_id, except_type):
    """
    raises the exception, clean up if needed
    :param thread_id: int
    :param except_type: type
    :return: None
    """
    thread_id = ctypes.c_long(thread_id)
    if not inspect.isclass(except_type):
        except_type = type(except_type)

    rst = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(except_type))

    if rst == 0:
        raise ValueError("Invalid thread id")
    elif rst != 1:
        """if it returns a number greater than one, you're in trouble, 
        and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    """
    stop thread
    :param thread: object
    :return: None
    """
    _async_raise(thread_id=thread.ident, except_type=SystemExit)


if __name__ == '__main__':
    my_thread = threading.Thread(target=say_hello)
    my_thread.start()

    input()
    stop_thread(thread=my_thread)
