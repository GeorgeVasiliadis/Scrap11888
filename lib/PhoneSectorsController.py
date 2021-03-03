import threading
from . import QueryMaker, Miner, Exporter, Filter

class PhoneSectorsController(threading.Thread):
    """
    This class is used to define the controller entity of Phone Sectors. It
    derives from Thread class in order to support more demanding queries. A user
    may start more than one queries in parallel.
    """

    def __init__(self, logger, name, location, address=""):
        super().__init__()
        self.logger = logger
        self.name = name
        self.location = location
        self.address = address
        self.filename = name + "_" + location
        if self.address: self.filename += "_" + self.address

    def run(self):
        """
        This method implements the actual query while defined as a unique thread.
        """

        self.logger.log("New Search", "info")

        raw_data = QueryMaker.query(self.name, self.location, self.logger)

        formatted_data = Miner.mine(raw_data)
        if not raw_data:
            self.logger.log("There are no results! No file will be generated!", "warning")
            return

        # Filter out data if and only if user has supplied an address.
        # This statement could be omitted - it's used only for optimization.
        if self.address:
            self.logger.log("Filtering out records that don't match {}...".format(self.address), "info")
            formatted_data = Filter.filter(formatted_data, self.address)

        if not formatted_data:
            self.logger.log("There are no results! No file will be generated!", "warning")
            return

        Exporter.exportToExcel(formatted_data, self.filename)

        self.logger.log("File has been succesfully exported as \"{}.xlsx\"!".format(self.filename), "success")
