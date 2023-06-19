from numpy import random

def powermeter_get(device=None):
    """
    So far dummy-function.
    Takes the name of the powermeter device and returns the current power.
    """
    if device is None:
        return random.random()

def counter_get(device=None):
    """
    So far dummy-function.
    Takes the name of the counter and returns the current counts. 
    """
    if device is None:
        return random.random(3)
    
