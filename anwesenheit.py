import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException


def show_confirmation_dialog(fach):
    result = messagebox.askyesno("Bestätigung", f"Anwesenheit für {fach} eintragen?",)
    if result:
        return True
    else:
        return False


csv_file = "loginfile.csv"

with open(csv_file, 'r') as csv_datei:
    # Erstelle einen CSV-Leser
    csv_leser = csv.reader(csv_datei)
    
    # Lies die erste Zeile der CSV-Datei (Annahme: Header)
    header = next(csv_leser)
    
    try:
        # Lies die nächste Zeile mit den Daten
        daten = next(csv_leser)
        
        # Trenne die Werte mit einem Komma und speichere sie in Variablen
        if len(daten) >= 2:
            wert1, wert2 = daten[0], daten[1]
        else:
            print("Nicht genügend Werte in der Zeile.")
    except StopIteration:
        print("Die CSV-Datei ist leer.")




#service = Service(executable_path='msedgedriver.exe')
#options = webdriver.EdgeOptions()
driver = webdriver.Firefox()

#----Bei Problemen mit textbox------------------
#options = webdriver.FirefoxOptions()
#options.headless = False  # Run the browser in non-headless mode
#driver = webdriver.Firefox(options=options)
#-----------------------------------------------


#service=service, options=options

#Später automatisieren https://stackoverflow.com/questions/50096474/get-links-from-a-certain-div-using-selenium-in-python
faecher  = [("Barcamp", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55418"), ("Informatik", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55128"),
            ("Linux Grundlagen", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55802"), ("MatheVO", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55855"),
            ("MatheUE", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55856"),("Netzwerktechnologien", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55580"),
            ("Software Development I", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=55669"),("Software Engineering Grundlagen", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=56461"),
            ("Teamentwicklung", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=57766"),("Webtechnologien", "https://elearning.fh-joanneum.at/mod/attendance/view.php?id=56408")]
# Öffnen Webseite
url = "https://elearning.fh-joanneum.at/my/"
driver.get(url)


#sign in----------------------------------------
elem = driver.find_element(By.ID, "username")
elem.send_keys(f"{wert1}")
elem = driver.find_element(By.ID, "password")
elem.send_keys(f"{wert2}")
elem = driver.find_element(By.ID, "loginbtn")
elem.click()
#-----------------------------------------------
#loop through faecher---------------------------
for fach, url in faecher:
    print(f"Fach: {fach}, URL: {url}")
    driver.get(url)
    
    try:
        # Try to find the element by the first link text
        anwesenheit_link = driver.find_element(By.LINK_TEXT, "Anwesenheit erfassen")
        print(f"Found element by 'Anwesenheit erfassen' link text.")
    except NoSuchElementException:
        try:
            # If the first link text is not found, try the second one
            anwesenheit_link = driver.find_element(By.LINK_TEXT, "Submit Attendance")
            print(f"Found element by 'Submit Attendance' link text.")
        except NoSuchElementException:
            print("Both link texts not found. Moving on to the next Fach.")
            continue
    
    try:
        time.sleep(2)
        anwesenheit_link.click()
        elem2 = driver.find_element(By.CLASS_NAME, "form-check-input")
        elem2.click()
        elem2 = driver.find_element(By.ID, "id_submitbutton")
        print(f"Anwesenheit eintragen gefunden in {fach}!")

        user_input = show_confirmation_dialog(fach)

        if user_input:
            elem2.click()
            time.sleep(5)
        else:
            continue
    except:
        print("ID 'anwesenheit' nicht gefunden. Gehe zum nächsten Fach.")
        continue
#-----------------------------------------------

driver.quit()
