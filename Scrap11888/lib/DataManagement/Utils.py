def purify(string):
    """
    This function simplifies the given string as much as possible and returns the
    pure version of it. It is supposed to work basically for Greek words, but
    other languages shouldn't cause trouble. Its actual operation includes removing
    all accents from given string, lowering all of its characters and removing
    leading and trailing spaces.
    It is useful when trying to compare two Greek words like "Γιώργος" and
    "  ΓΙΩΡΓΟΣ " - although they don't match in an absolute way, it might be
    useful to consider them equal.

    - string: The string to be purified.
    """

    # Map all possible characters with accents to their simplified version
    # 'ς' is included as exception because `.lower()` won't work in that manner.
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
        "ώ": "ω",
        "ς": "σ"
    }

    pure = ""

    # Apply changes only to a non-empty string
    if string:
        pure = string.lower().strip()

        for letter in pure:
            if letter in dict.keys():
                pure = pure.replace(letter, dict[letter])

    return pure
