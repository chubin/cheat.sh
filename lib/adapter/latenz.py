import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from globals import PATH_LATENZ
from adapter import Adapter

class Latenz(Adapter):

    _adapter_name = "late.nz"
    _output_format = "ansi"
    _repository_url = "https://github.com/chubin/late.nz"

    def _get_page(self, topic, request_options=None):
        sys.path.append(PATH_LATENZ)
        import latencies
        return latencies.render()

    def _get_list(self, prefix=None):
        return ['latencies']

    def is_found(self, topic):
        return topic.lower() in ['latencies', 'late.nz', 'latency']
