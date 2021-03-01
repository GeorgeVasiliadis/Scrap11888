from openpyxl import Workbook
import json

#with open(f_out+".json", "w", encoding="utf-8") as file:
#    file.write(json.dumps(raw_data, ensure_ascii=False, indent=2))

def prepare(raw_data):
    formattedRecords = []

    for record in raw_data:
        new_rec = {
            "id": None,
            "name": None,
            "address": None,
            "number": None
            }

        # INDEX
        if "index" in record:
            new_rec["id"] = record["index"]

        # NAME
        if "name" in record:
            if "last" in record["name"] and record["name"]["last"]:
                new_rec["name"] = record["name"]["last"]
                if "middle" in record["name"] and record["name"]["middle"]:
                    new_rec["name"] += " " + record["name"]["middle"]
                if "first" in record["name"] and record["name"]["first"]:
                    new_rec["name"] += " " + record["name"]["first"]
            elif "first" in record["name"] and record["name"]["first"]:
                new_rec["name"] = record["name"]["first"]

        # ADDRESS
        if "address" in record and record["address"]:
            if "street1" in record["address"] and record["address"]["street1"]:
                new_rec["address"] = record["address"]["street1"]
                if "number1" in record["address"] and record["address"]["number1"]:
                    new_rec["address"] += " " + record["address"]["number1"]
        formattedRecords.append(new_rec)

        # PHONES
        if "phones" in record and record["phones"]:
            if "number" in record["phones"][0] and record["phones"][0]["number"]:
                new_rec["number"] = record["phones"][0]["number"]

    return formattedRecords

def purify(address):
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
    if address:
        pure = address.lower().strip()
        for letter in address:
            if letter in dict.keys():
                pure = pure.replace(letter, dict[letter])
    return pure

def mineToExcel(raw_data, f_out, address="", logger=None):
    data = prepare(raw_data)
    if data:
        workbook = Workbook()
        sheet = workbook.active

        sheet["A1"] = "Αριθμός Εγγραφής"
        sheet["B1"] = "Όνομα"
        sheet["C1"] = "Διεύθυνση"
        sheet["D1"] = "Τηλέφωνο"

        row = 2
        for record in data:

            if address:
                if not purify(address) in purify(record["address"]):
                    continue

            sheet["A"+str(row)] = record["id"]
            sheet["B"+str(row)] = record["name"]
            sheet["C"+str(row)] = record["address"]
            sheet["D"+str(row)] = record["number"]
            row += 1
        workbook.save(filename=f_out+".xlsx")

        if logger: logger.log("Data have been successfully exported as {}.xlsx!".format(f_out), "success")
        print("Data have been successfully exported as {}.xlsx!".format(f_out))
    else:
        if logger: logger.log("No data to be exported!", "warning")
        print("There are no data to be exported!")
