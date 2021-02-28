from bs4 import BeautifulSoup
from openpyxl import Workbook
import os

def scrapeHtml():
    agenda = []
    pages = []

    for file in os.listdir():
        if ".html" in file: pages.append(file)

    for src in pages:

        with open(src, "r", encoding="utf-8") as file: html = file.read()
        os.remove(src)
        soup = BeautifulSoup(html, "html.parser")

        ls = soup.findAll("div", {"class":"search-card media listing-item no-img"})
        for item in ls: 
            ID = item.find("span", {"class":"corner"}).text
            address = item.find("p", {"class":"loc"}).text
            name = item.find("h2").text
            phone = item.find("ul", {"class":"dropdown-menu no-before"}).text
            agenda.append([ID, address, name, phone])
        



            
    workbook = Workbook()
    sheet = workbook.active

    letters = ["A", "B", "C", "D"]

    for index, entry in enumerate(agenda, 1):
        for i in range(4):
            key = letters[i] + str(index)
            sheet[key] = entry[i]
                
    workbook.save(filename="Phone_Sectors_Data.xlsx")
    os.rename("Phone_Sectors_Data.xlsx", "../Phone_Sectors_Data.xlsx")
