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

        for letter in pure:
            if letter in dict.keys():
                pure = pure.replace(letter, dict[letter])

    return pure

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
