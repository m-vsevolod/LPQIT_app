from numpy import random
from time import sleep
from serial import Serial
   
def open_serial(port, baudrate=None, TEST=False, comments=False):
    """
    A function to connect a device. 
    If TEST = TRUE, than returns None. 
    If comments = False, than nothing will be printed.
    """
    if TEST:
        if comments : print(f"Port {port} is connected. (TEST)")
        return None
    else:
        if baudrate == None:
            try:
                if comments : print(f"Port {port} is connected.")
                return Serial(port)
            except Exception as e:
                if comments : print(f"Port {port} was not connected. Error: " + str(e))
                return None
        else:
            try:
                if comments : print(f"Port {port} is connected.")
                return Serial(port, baudrate)
            except Exception as e:
                if comments : print(f"Port {port} was not connected. Error: " + str(e))
                return None
            
def close_serial(*devices, TEST=False, comments=False):
    """
    A function to close serial devices.
    If TEST=True, than returns None.
    If comments = False, than nothing will be printed.
    """
    if TEST:
        if comments : print("Serial devices are closed. (TEST)")
        return None
    else:
        for device in devices:
            try:
                if comments : print(f"{device} is now closed.")
                device.close()
            except Exception as e:
                if comments : print(f"Failed to close {device}. Error: " + str(e))

def turn_curtain(curtain_device, angle, TEST = False, comments=False):
    """
    A function to turn the curtain. 
    If TEST=True, than returns None. 
    If comments = False, than nothing will be printed.
    """
    if TEST:
        if comments : print(f"The curtain turned at an {angle}. (TEST)")
        return None
    else:
        try:
            command = str(angle)
            if comments : print(f"The curtain turned at an {angle}")
            curtain_device.write(command.encode('utf-8'))
        except Exception as e:
            if comments : print("Curtain failed to turn. Error :" + str(e))
            return None

def d_action(d_device, TEST = False, comments=False):
    """
    A function to talk with the diaphragm. 
    If TEST=True, than returns None. 
    If comments = False, than nothing will be printed.
    """
    if TEST:
        if comments : print("Diaphragm recieved the message. (TEST)")
    else:
        try:
            if comments : print("Diaphragm recieved the message.")
            values = bytes.fromhex('111140014400000000001111400153000A0000001111400150004600000011114001470000000000')
            d_device.write(values)
            return None
        except Exception as e:
            if comments : print("Failed to send a command to a diaphragm. Error code : " + str(e))
            return None

def read_counts(counter_device, TEST = False, comments=False):
    """
    A function to read the counts of the SPD. 
    If TEST = True, than 3 random numbers will be returned.
    If comments = False, than nothing will be printed.
    """
    if TEST:
        if comments : print("3 random numbers generated. (TEST)")
        return random.randint(low=0, high=100, size=3)
    else:
        try:
            if comments : print("Count numbers were recieved.")
            raw_reading = counter_device.readline().decode(errors='ignore')
            return [int(part.strip()) for part in raw_reading.split('\t')] 
        except Exception as e:
            if comments : print("Failed to recieve count numbers. Error : " + str(e))
            return None
        
def read_power(powermeter_device, TEST=False, comments=False):
    """
    A function to read the power from the powermeter.
    If TEST = True, than random number will be returned.
    If comments = False, than nothing will be printed. 
    """
    if TEST:
        if comments : print("Random number generated. (TEST)")
        return random.random()
    else:
        try:
            powermeter_device.write(b'*CVU')
            temp = powermeter_device.readline().decode().strip()
            if comments : print(f"Power recieved: {temp}")
            return temp
        except Exception as e:
            if comments : print("Failed to measure the power. Error : " + str(e))
            return None