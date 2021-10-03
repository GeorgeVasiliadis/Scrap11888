import threading
import concurrent.futures

from .Fetching import QueryMaker
from .DataManagement import  Miner, Exporter, Filter, Cacher

class Controller(threading.Thread):
    """
    This class is used to define the controller entity of Scrap11888. It
    derives from Thread class in order to support more demanding queries. A user
    may start more than one queries in parallel.
    """

    def __init__(self, logger, names, location, address=""):
        super().__init__()
        if len(names) > 1: self.multi = True
        else: self.multi = False
        self.logger = logger
        self.names = names
        self.location = location
        self.address = address

    def thready(name, location, address, multi, logger):
        if name:

            # Try to find requested data in cache
            formatted_data = Cacher.cacheOut(location, name)

            # If requested data are not cached, fetch them
            if not formatted_data:
                logger.log("New Search for {}.".format(name), "info")
                raw_data = QueryMaker.query(name, location, logger)
                formatted_data = Miner.mine(raw_data)

                if not formatted_data and not multi:
                    logger.log("There are no results! No file will be generated!", "warning")
                    return

                # Cache the fetched, well-formatted data
                Cacher.cacheIn(location, name, formatted_data)

            # Filter out data if and only if user has supplied an address.
            # This statement could be omitted - it's used only for optimization.
            if address:
                logger.log("Filtering out records that don't match {}...".format(address), "info")
                formatted_data = Filter.filter(formatted_data, address)

            if not formatted_data and not multi:
                logger.log("There are no results! No file will be generated!", "warning")
                return

            filename = defineFilename(name, location, address)

            isExported = Exporter.exportToExcel(formatted_data, filename)

            if isExported:
                logger.log(f"File \"{filename}.xlsx\" has been created!", "success")
            else:
                logger.log("No file was created. There are no data to be exported.", "warning")

        else:
            logger.log("Empty name.", "warning")

    from .Decorators.Debugging import timeMe
    @timeMe
    def run(self):
        """
        This method implements the actual query defined as a unique thread.
        """

        with concurrent.futures.ThreadPoolExecutor(max_workers=45) as executor:
            for name in self.names:
                executor.submit(Controller.thready, name, self.location, self.address, self.multi, self.logger)

        self.logger.log("DONE", "info")

def defineFilename(name, location, address):
    filename = name + "_" + location
    if address: filename += "_" + address
    return filename
