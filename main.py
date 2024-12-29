#huom. tässä luetaan ladatulta sivulta, jos haluat ajankohtaisen tiedon , nettisivu pitää päivittää

import requests  #lukee sivun tekstinä
import selectorlib  # valitsee sivulta
import send_email
import time

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# headers lisätään, ellei scrape muuten toimi (kopioitiin UDEMYn ohjeista). Auttaa myös, jos sivu ei hyväksy scriptejä

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

def store(extracter):
    with open("data.txt", "a") as file:  #a lisää w kirjoittaa päälle
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    while True:
        #print(scrape(URL)) voi kokeilla ennen alla olevaa
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email.send_email(message="Hey, new event was found!")
    time.sleep(2) #tsekkaa 2 sek välein
