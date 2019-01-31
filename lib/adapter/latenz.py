import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from globals import PATH_LATENZ

def get_answer(topic, request_options=None):
    sys.path.append(PATH_LATENZ)
    import latencies
    return latencies.render()

def get_list():
    return ['latencies']

def is_found(topic):
    return topic.lower() in ['latencies', 'late.nz', 'latency']
