#huom. tässä luetaan ladatulta sivulta, jos haluat ajankohtaisen tiedon , nettisivu pitää päivittää

import requests  #lukee sivun tekstinä
import selectorlib  # valitsee sivulta
import send_email
import time
import sqlite3




URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# headers lisätään, ellei scrape muuten toimi (kopioitiin UDEMYn ohjeista). Auttaa myös, jos sivu ei hyväksy scriptejä

connection = sqlite3.connect("data1.db")

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS) # headers jos tehtiin lisäys
    source = response.text   #lukee tekstin
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml") #Extractor on class, extract.yaml tehdään itse
    #extract.yaml ilmoittaa mitä kohtaa haetaan
    value = extractor.extract(source)["tours"] # key extract.yaml:ssä, voi olla mikä vaan
    return value

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO event VALUES(?,?,?)", row) # row on 3 olion lista
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM event WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows
    #with open("data.txt", "r") as file:
    #    return file.read()
    #rivejä kopioitiin example.py tiedostosta


if __name__ == "__main__":
    while True:
        #print(scrape(URL)) voi kokeilla ennen alla olevaa
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if  not row:  #empty list on false
                store(extracted)
                send_email.send_email(message="Hey, new event was found!")
    time.sleep(2) #tsekkaa 2 sek välein
