from lib.DataManagement.__init__ import purify

def filter(data, key):
    """
    This function is used to filter out all records that don't match to given
    key. In current implementation filter is applied on address field.
    - data: The formatted data to be filtered.
    - key: The srting that should be contained in a record's address.
    """

    filtered_data = []

    key = purify(key)

    for record in data:
        if key in purify(record["address"]):
            filtered_data.append(record)

    return filtered_data
