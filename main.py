from selenium import webdriver
from bs4 import BeautifulSoup
import os, shutil
from termcolor2 import c
from requests import get
import colorama
colorama.init()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
print(c("""
 ___   __  __ _  ___  _ 
| __| |  \/  | |/ / || |
| _| _| |\/| | ' <| __ |
|___(_)_|  |_|_|\_\_||_|  
""").red)
print(c("Kumw6.com Downloader Coded By E.MKH - @EsMailMKH").green)

while True:
    url = input(c("Enter Url of Chapter From kumw6.com: ").yellow)
    if url == 'e':
        print("bye bye")
        driver.close()
    print("[Start Leeching Images...]")

    driver.get(url)
    print("[Leeching Completed!]\n")
    title = driver.title
    soup = BeautifulSoup(driver.page_source, "html.parser")
    div_main = soup.find("div", {"class": "main_img"})
    images = []
    for img in div_main.find_all("img"):
        if img['src'] != "/static/images/load.gif":
            images.append(img['src'])
        else:
            images.append(img['data-src'])
    print("[Start Downloading Images...]")

    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        
        
    if os.path.exists("downloads/" + title):
        print(c("This chapter is already in the downloads folder, make sure that it has been deleted or enter another chapter url!\n").red)
    else:
        if not os.path.exists("downloads/" + title):
            os.mkdir("downloads/" + title)
        count = 0
        for img in images:
            count += 1
            
            if len(images) < 10:
                filename = str(count).zfill(2)
            elif len(images) < 100:
                filename = str(count).zfill(3)
            elif len(images) < 1000:
                filename = str(count).zfill(4)
            elif len(images) < 10000:
                filename = str(count).zfill(5)
                
            r = get(img, stream=True)
            path = "downloads/" + title + "/" + filename
            with open(f"{path}.jpg", "wb") as out_file:
                shutil.copyfileobj(r.raw, out_file)
            print(c(f"Status: [Image {count}/{len(images)}] - [{round(count * 100 / len(images), 2)}%]").cyan, end="\r")
            
        print(c("\nDownload Successfully Completed!").green)
        print(c(f"Your Download Saved in {title} in downloads folder\n").green)
