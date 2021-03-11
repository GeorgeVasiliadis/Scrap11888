import threading
import concurrent.futures

from .Fetching import QueryMaker
from .DataManagement import  Miner, Exporter, Filter, Cacher

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
        # if not self.multi: self.filename = self.names[0]
        # else: self.filename = "Range"
        # self.filename += "_" + self.location
        # if self.address: self.filename += "_" + self.address
        self.filename = self.names[0]
        self.filename += "_" + self.location

    from lib.Decorators.Debugging import timeMe

    def thready(name, location, address, multi, logger):
        if name:
            logger.log("New Search for {}.".format(name), "info")

            formatted_data = Cacher.cacheOut(location, name)
            if not formatted_data:

                raw_data = QueryMaker.query(name, location, logger)

                formatted_data = Miner.mine(raw_data)
                if not raw_data and not multi:
                    logger.log("There are no results! No file will be generated!", "warning")
                    return
                Cacher.cacheIn(location, name, formatted_data)

            # Filter out data if and only if user has supplied an address.
            # This statement could be omitted - it's used only for optimization.
            if address:
                logger.log("Filtering out records that don't match {}...".format(address), "info")
                formatted_data = Filter.filter(formatted_data, address)

            if not formatted_data and not multi:
                logger.log("There are no results! No file will be generated!", "warning")
                return

            filename = f"{name}_{location}"
            isExported = Exporter.exportToExcel(formatted_data, filename)

        else:
            logger.log("Empty name.", "warning")

    @timeMe
    def run(self):
        """
        This method implements the actual query defined as a unique thread.
        """

        with concurrent.futures.ThreadPoolExecutor(max_workers=45) as executor:
            for name in self.names:
                executor.submit(PhoneSectorsController.thready, name, self.location, self.address, self.multi, self.logger)

        self.logger.log("DONE", "info")
        # if isExported:
        #     self.logger.log("File has been succesfully exported as \"{}.xlsx\"!".format(self.filename), "success")
        # else:
        #     self.logger.log("No file was created. There are no data to be exported.", "warning")
