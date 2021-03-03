from openpyxl import Workbook

def exportToExcel(formatted_data, f_out):
    """
    This function exports well-formatted data into an excel file. If the dataset
    is empty, no file will be created.
    - formatted_data: The data to be exported.
    - f_out: The name of the file to be created.
    """

    # Ensure that the dataset is not empty
    if formatted_data:
        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"] = "Αριθμός Εγγραφής"
        sheet["B1"] = "Όνομα"
        sheet["C1"] = "Διεύθυνση"
        sheet["D1"] = "Τηλέφωνο"

        for row, record in enumerate(formatted_data, 2):
            sheet["A"+str(row)] = record["id"]
            sheet["B"+str(row)] = record["name"]
            sheet["C"+str(row)] = record["address"]
            sheet["D"+str(row)] = record["number"]

        workbook.save(filename=f_out+".xlsx")
