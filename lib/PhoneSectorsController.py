import threading
from . import QueryMaker, Miner, Exporter, Filter

class PhoneSectorsController(threading.Thread):
    """
    This class is used to define the controller entity of Phone Sectors. It
    derives from Thread class in order to support more demanding queries. A user
    may start more than one queries in parallel.
    """

    def __init__(self, logger, names, location, address=""):
        super().__init__()
        self.multi = False
        if len(names) > 1: self.multi = True
        self.logger = logger
        self.names = names
        self.location = location
        self.address = address
        self.initFilename()

    def initFilename(self):
        if not self.multi: self.filename = self.names[0]
        else: self.filename = "Range"
        self.filename += "_" + self.location
        if self.address: self.filename += "_" + self.address

    def run(self):
        """
        This method implements the actual query defined as a unique thread.
        """

        append=False
        for name in self.names:
            if name:
                self.logger.log("New Search for {}.".format(name), "info")

                raw_data = QueryMaker.query(name, self.location, self.logger)

                formatted_data = Miner.mine(raw_data)
                if not raw_data and not self.multi:
                    self.logger.log("There are no results! No file will be generated!", "warning")
                    return

                # Filter out data if and only if user has supplied an address.
                # This statement could be omitted - it's used only for optimization.
                if self.address:
                    self.logger.log("Filtering out records that don't match {}...".format(self.address), "info")
                    formatted_data = Filter.filter(formatted_data, self.address)

                if not formatted_data and not self.multi:
                    self.logger.log("There are no results! No file will be generated!", "warning")
                    return

                isExported = Exporter.exportToExcel(formatted_data, self.filename, append)
                if not append and isExported:
                    append = not append

            else:
                self.logger.log("Empty name.", "warning")

        if append:
            self.logger.log("File has been succesfully exported as \"{}.xlsx\"!".format(self.filename), "success")
        else:
            self.logger.log("No file was created. There are no data to be exported.", "warning")
