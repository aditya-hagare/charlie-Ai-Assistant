import threading

_interrupt_event = threading.Event()

def interrupt():
    _interrupt_event.set()

def clear_interrupt():
    _interrupt_event.clear()

def is_interrupted():
    return _interrupt_event.is_set()
