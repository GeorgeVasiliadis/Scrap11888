import QueryMaker, Miner, Exporter

class PhoneSectorsController:
    def __init__(self):
        pass

    def extractData(self, name, location, address=""):
        filename = name + "_" + location
        if address: filename += "_" + address
        raw_data = qm.query(name, location)
        formatted_data = Miner.mine(raw_data)
        Exporter.exportToExcel(formatted_data, filename)
