import requests
import concurrent.futures

def fetchPage(name, location, page=None):
    """Try to fetch the page corresponding to a query search with specified
    parameters. If there is no such page, or in case of error, None will be
    returned.
    If provided, page will specify the desired page - it may not exist on the
    actual data.

    - name: A string of the desired name
    - location: A string of the desired location
    - page: A sting of the desired page
    """

    url = "https://www.11888.gr/search/white_pages/?&query={}&location={}".format(name, location)

    if page:
        url += "&page={}".format(page)

    response = requests.get(url)

    if response.ok:
        return response

    return None

def findPageCount(name, location, logger):
    """
    This function queries and retrieves the number of pages of 11888.gr results
    for the specific search parameters. If the parameters are faulty or lead to
    no results, the page count is zero.

    - name: A string of the desired name to be searched.
    - location: A string of the desired name to be searched.
    """

    count = 0
    response = fetchPage(name, location)

    if not response:
        logger.log("An error has occured while trying to calculate count of records from 11888.gr", "error")
    else:
        if "data" in response.json():
            if "total_pages" in response.json()["data"]:
                count = response.json()["data"]["total_pages"]

    return count

def thready(name, location, page, records, logger):
    """This function is ment to be called as part of a thread pool executor.
    It downloads the data and appends them to given recordList.
    """

    logger.log("Working on page {}...".format(page), "info")

    response = fetchPage(name, location, page)
    if not response:
        logger.log("An error has occured while trying to fetch data from 11888.gr", "error")
    else:
        logger.log("Page {} has been fetched successfully!".format(page), "info")
        if "data" in response.json():
            if "results" in response.json()["data"]:
                for record in response.json()["data"]["results"]:
                    records.append(record)

def query(name, location, logger):
    """
    This function queries the name dictionary of 11888.gr for a specific name, in
    a specific location. It returns a .json formatted dataset containing all
    sorts of information about the people that are being searched. Thus, the
    returned data could be considered as "raw data".

    - name: A string of the desired name to be searched.
    - location: A string of the desired name to be searched.
    """

    # Set of data retrieved from each page, combined in one list
    records = []
    recordCount = findPageCount(name, location, logger)

    if recordCount:
        logger.log("Pages to be fetched: {}".format(recordCount), "warning")

    # Query each one of the pages of 11888.gr and retrieve the contained .json data.
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        for page in range(recordCount):
            executor.submit(thready, name, location, page, records, logger)

    return records
