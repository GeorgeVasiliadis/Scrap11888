def mine(raw_data):
    """
    This function transforms an already strictly formatted set of .json data
    into a useful list of records in a specific format. Badly formatted data may
    lead to an empty list being returned.

    - raw_data: The .json data as retrieved from 11888.gr to be formatted.
    """

    # List of formatted data
    records = []

    for record in raw_data:

        # Template: Create an empty dictionary-record
        new_rec = {
            "id": None,
            "name": None,
            "street": None,
            "streetNumber": None,
            "phoneNumber": None
        }

        # Isolate Index
        if "index" in record:
            new_rec["id"] = record["index"]

        # Isolate Name
        if "name" in record:
            if "last" in record["name"] and record["name"]["last"]:
                new_rec["name"] = record["name"]["last"]
                if "middle" in record["name"] and record["name"]["middle"]:
                    new_rec["name"] += " " + record["name"]["middle"]
                if "first" in record["name"] and record["name"]["first"]:
                    new_rec["name"] += " " + record["name"]["first"]
            elif "first" in record["name"] and record["name"]["first"]:
                new_rec["name"] = record["name"]["first"]

        # Isolate Address
        if "address" in record and record["address"]:
            if "street1" in record["address"] and record["address"]["street1"]:
                new_rec["street"] = record["address"]["street1"]
                if "number1" in record["address"] and record["address"]["number1"]:
                    new_rec["streetNumber"] = record["address"]["number1"]

        # Isolate Phone
        if "phones" in record and record["phones"]:
            if "number" in record["phones"][0] and record["phones"][0]["number"]:
                new_rec["phoneNumber"] = record["phones"][0]["number"]

        records.append(new_rec)

    return records
