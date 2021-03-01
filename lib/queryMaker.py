import requests

def findPageCount(name, location, logger=None):
    count = 0
    response = requests.get("https://www.11888.gr/search/white_pages/?&query={}&location={}".format(name, location))
    if not (response.status_code == requests.codes.ok):
        if logger: logger.log("An error has occured while trying to calculate count of records from 11888.gr", "error")
        print("An error has occured while trying to calculate count of records from 11888.gr")
    else:
        if "data" in response.json():
            if "total_pages" in response.json()["data"]:
                count = response.json()["data"]["total_pages"]
    return count


def query(name, location, logger=None):
    records = []
    recordCount = findPageCount(name, location, logger)
    for page in range(recordCount):
        if logger: logger.log("Working on page {}...".format(page), "info")
        print("Working on page {}...".format(page))
        response = requests.get("https://www.11888.gr/search/white_pages/?&query={}&location={}&page={}".format(name, location, page))
        if not (response.status_code == requests.codes.ok):
            if logger: logger.log("An error has occured while trying to fetch data from 11888.gr", "error")
            print("An error has occured while trying to fetch data from 11888.gr")
        else:
            if logger: logger.log("Data have been successfully fetched!", "success")
            print("Data have been successfully fetched!")
            if "data" in response.json():
                if "results" in response.json()["data"]:
                    for record in response.json()["data"]["results"]:
                        records.append(record)

    return records
