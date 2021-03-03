import threading
from . import QueryMaker, Miner, Exporter, Filter

class PhoneSectorsController(threading.Thread):
    """
    This class is used to define the controller entity of Phone Sectors. It
    derives from Thread class in order to support more demanding queries. A user
    may start more than one queries in parallel.
    """

    def __init__(self, name, location, address=""):
        super().__init__()
        self.name = name
        self.location = location
        self.address = address
        self.filename = name + "_" + location
        if self.address: self.filename += "_" + self.address

    def run(self):
        """
        This method implements the actual query while defined as a unique thread.
        """

        raw_data = QueryMaker.query(self.name, self.location)
        formatted_data = Miner.mine(raw_data)

        # Filter out data if and only if user has supplied an address.
        # This statement could be omitted - it's used only for optimization.
        if self.address:
            formatted_data = Filter.filter(formatted_data, self.address)

        Exporter.exportToExcel(formatted_data, self.filename)
