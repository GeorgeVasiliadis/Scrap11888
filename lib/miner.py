def purify(string):
    """
    This function simplifies the given string as much as possible and returns the
    pure version of it. It is supposed to work basically for Greek words, but
    other languages will not cause trouble. Its actual operation includes removing
    all accents from given string, lowering all of its characters and removing
    leading and trailing spaces.
    It is useful when trying to compare two Greek words like "Γιώργος" and
    "ΓΙΩΡΓΟΣ" - although they don't match, it might be useful to be consider them
    equal.
    - string: The string to be purified.
    """

    # Map all possible characters with accents to their simplified version
    dict = {
        "ά": "α",
        "έ": "ε",
        "ή": "η",
        "ί": "ι",
        "ϊ": "ι",
        "ΐ": "ι",
        "ό": "ο",
        "ύ": "υ",
        "ϋ": "υ",
        "ΰ": "υ",
        "ώ": "ω"
    }

    pure = ""

    # Apply changes only to a non-empty string
    if string:
        pure = string.lower().strip()

        for letter in string:
            if string in dict.keys():
                pure = pure.replace(letter, dict[letter])

    return pure

def mine(raw_data):
    """
    This function transforms an already strictly formatted set of .json data
    into a useful list of records in a specific format.
    - raw_data: The .json data as retrieved from 11888.gr to be formatted.
    """

    # List of formatted data
    records = []

    for record in raw_data:

        # Create a templated empty dictionary-record
        new_rec = {
            "id": None,
            "name": None,
            "address": None,
            "number": None
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
                new_rec["address"] = record["address"]["street1"]
                if "number1" in record["address"] and record["address"]["number1"]:
                    new_rec["address"] += " " + record["address"]["number1"]

        # Isolate Phone
        if "phones" in record and record["phones"]:
            if "number" in record["phones"][0] and record["phones"][0]["number"]:
                new_rec["number"] = record["phones"][0]["number"]

        records.append(new_rec)

    return records
