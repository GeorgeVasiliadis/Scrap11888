import requests

def findPageCount(name, location, logger):
    """
    This function queries and retrieves the number of pages of 11888.gr results
    for the specific search parameters. If the parameters are faulty of lead to
    no results, the page count is zero.
    - name: A string of the desired name to be searched.
    - location: A string of the desired name to be searched.
    """

    count = 0
    response = requests.get("https://www.11888.gr/search/white_pages/?&query={}&location={}".format(name, location))

    if not (response.status_code == requests.codes.ok):
        logger.log("An error has occured while trying to calculate count of records from 11888.gr", "error")
    else:
        if "data" in response.json():
            if "total_pages" in response.json()["data"]:
                count = response.json()["data"]["total_pages"]

    return count

# TODO: this function makes N queries to 11888.gr (N = the number of pages
# returned).
# This could possibly be optimized to return all data in one single page.
# Consider engineering "&records=N" to query.
def query(name, location, logger):
    """
    This function queries the name dictionary of 11888.gr for a specific name, in
    a specific location. It returns a .json formatted dataset containing all
    sorts of information about the people that are being searched. Thus, the
    returned data is could be considered as "raw data".
    - name: A string of the desired name to be searched.
    - location: A string of the desired name to be searched.
    """

    # Set of data retrieved from each page, combined in one list
    records = []
    recordCount = findPageCount(name, location, logger)

    if recordCount:
        logger.log("Pages to be fetched: {}".format(recordCount), "warning")

    # Query each one of the pages of 11888.gr and retrieve the contained .json data.
    for page in range(recordCount):

        logger.log("Working on page {}...".format(page), "info")

        response = requests.get("https://www.11888.gr/search/white_pages/?&query={}&location={}&page={}".format(name, location, page))

        if not (response.status_code == requests.codes.ok):
            logger.log("An error has occured while trying to fetch data from 11888.gr", "error")
        else:
            logger.log("Data have been successfully fetched!", "info")
            if "data" in response.json():
                if "results" in response.json()["data"]:
                    for record in response.json()["data"]["results"]:
                        records.append(record)

    return records
