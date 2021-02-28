import HTML_dLoader as dLoader
import Data_Scraper as ds

while True:
    ans = input("Copy from your browser the NAME KEY and paste it here: ")
    if len(ans) >= 3:
        name = ans
        break
    else: print("Please insert a NAME KEY longer than 3 characters")

while True:
    ans = input("Copy from your browser the LOCATION KEY and paste it here: ")
    if ans != "":
        location = ans
        break
    else: print("Make sure you copy the LOCATION KEY")

while True:
    ans = input("Start from page: ")
    if ans.isnumeric():
        ans = int(ans)
        if ans >= 1:
            start_num = ans-1
            break
        else: print("Integer must be greater than zero")
    else: print("Please insert a number")

while True:
    ans = input("Stop at page (inclusive): ")
    if ans.isnumeric():
        ans = int(ans)
        stop_num = ans-1
        break
    else: print("Please insert a number")

dLoader.downloadHtml(name, location, start_num, stop_num)
ds.scrapeHtml()
