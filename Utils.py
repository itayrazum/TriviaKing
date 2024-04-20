import socket
import config
import random

def get_wifi_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        wifi_ip = s.getsockname()[0]

        # Close the socket
        s.close()

        return wifi_ip
    except Exception as e:
        print("Error occurred:", e)
        return None

def get_and_remove_name():
    """
    Gets a random name from the config.py list and removes it to prevent duplicates.

    :return: A random name from the list, or None if the list is empty.
    """
    if not config.names:
        return None  # List is empty

    chosen_name = random.choice(config.names)
    config.names.remove(chosen_name)
    return chosen_name

import time

