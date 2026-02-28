pending_action = None

def set_pending(action):
    global pending_action
    pending_action = action

def get_pending():
    return pending_action

def clear_pending():
    global pending_action
    pending_action = None
