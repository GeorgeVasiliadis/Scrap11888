from selenium import webdriver

def downloadHtml(name, location, start, stop):
    #--------URL--BUILDER-------#
    NAME_STRING = name
    LOCATION_STRING = location


    url_part1 = "https://www.11888.gr/white-pages/"
    url_part2 =  "/?query="
    url_part3 = "&location="
    url_part4 = "&page="
    URL = url_part1 + NAME_STRING + url_part2 + NAME_STRING + url_part3 + LOCATION_STRING + url_part4
    #-----------------------------------#

    versions = ["81", "80", "79"]
    path = "./Drivers/chromedriver"
    for v in versions:
        try:
            driver = webdriver.Chrome(path + v + ".exe")
            break
        except: print("Invalid Driver")
        
    for page in range(start, stop+1):
        PAGE_ID = str(page)
        driver.get(URL + PAGE_ID)
        fout = NAME_STRING + "_" + LOCATION_STRING +  "_" + PAGE_ID + ".html"
        with open(fout, "w", encoding="utf-8") as file: file.write(driver.page_source)

    driver.quit()
    
