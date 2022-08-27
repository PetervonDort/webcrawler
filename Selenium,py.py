from selenium import webdriver
import sqlite3 ,  locale
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#Variablen
WINDOW_SIZE = "1920,1080"
c = Options()
c.add_argument("--headless")
driver = webdriver.Chrome(options=c)
Wert = []
wait = 2
aktuelleWoche = date.today().strftime("%W")
aktuellerTag = date.today().strftime("%a")
aktuelleStunde = time.strftime('%H')
locale.setlocale(locale.LC_ALL, '')
hour = int(aktuelleStunde)
alterWert =0
Differenz =0


#Klassen
class ClDataBase():
    """ Diese Klasse dient der MYSQLLight Datenbank um die Daten entgegenzunehmen,verwalten  und zu speichern"""


    def __init__(self):
        # Unter Informationen werden Weblinks zu Börseninformationen gespeichert, Prognose soll den errechneten Preis abbilden
        # Tagestyp wird den Tag im ganzen bewerten (z.B: 0=normaler Tag,1 Fallender Kurs etc.)
        # Vorhersage Index Hier wird abgebildet wie die Tatsächliche Kursentwicklung vom vorhergesagten Kurs abweicht
        # z.b. -5 für einen um 5 Cent niedrigeren Kurs 5 wäre entsprechend ein höherer Kurs
        verbindung =sqlite3.connect("/home/peter/Dokumente/Datenbanken/boerseRechner.db")
        zeiger = verbindung.cursor()
        sql_anweisung =""" 
        CREATE TABLE IF NOT EXISTS Kurse(
        Woche INT(3),
        Tag TEXT(3),
        Stunde INT(2),
        Minute INT(2),
        Sekunde INT(2),        
        VKPreis REAL(5),
        EKPreis REAL(5),
        Differenz REAL(2),
        HoestPreis REAL(5),
        TiefPreis REAL (5)      
        );"""
        zeiger.execute(sql_anweisung)



    def meKursupload(self, Woche, Tag, Stunde, Minute, Sekunde, VK, EK, Diff, HoePr, NiPr):
        verbindung = sqlite3.connect("/home/peter/Dokumente/Datenbanken/boerseRechner.db")
        zeiger = verbindung.cursor()
        zeiger.execute( """
        INSERT INTO Kurse VALUES(?,?,?,?,?,?,?,?,?,?)""",
                        (Woche, Tag, Stunde, Minute, Sekunde, VK, EK, Diff, HoePr, NiPr))
        verbindung.commit()
        verbindung.close()


class ClContentGrab():
    def __init__(self):

        driver.get('https://www.boerse-stuttgart.de/de-de/produkte/aktien/stuttgart/555750-deutsche-telekom')
        driver.find_element(By.XPATH, "/html/body/aside/div[2]/div[2]/button[1]").click()

    def meGrab(self):
        contList = []
        content = driver.find_elements(By.CLASS_NAME, "bsg-card--course-data .bsg-card__value")
        for con in content:
            contList.append(con.text)
        return(contList)

    def meClose(self):
        driver.close()




#Hauptschleife

DataB = ClDataBase()
Content = ClContentGrab()

while hour >7 :#and  hour <18:
    aktuelleStunde = time.strftime('%H')
    aktuelleMinute = time.strftime('%M')
    aktuelleSekunde = time.strftime('%S')
    hour = int(aktuelleStunde)
    if hour >16:
        wait = 60
    time.sleep(2)
    Differenz =alterWert
    Wert = Content.meGrab()
    for nu in Wert:
        if nu == Wert[3] or Wert[2]:# Das macht noch alles wieder kaputt
            break
        else:
            if nu == '-' or nu == "%":
                nu = 0.0
            else:
                nu = locale.atof(nu)
    print(Wert)
    Differenz = Differenz-alterWert
    DataB.meKursupload(aktuelleWoche,aktuellerTag,aktuelleStunde,aktuelleMinute,aktuelleSekunde,locale.atof(Wert[0]), locale.atof(Wert[1]), Differenz, locale.atof(Wert[4]),locale.atof(Wert[5]))
    print(aktuelleWoche,aktuellerTag,aktuelleStunde,aktuelleMinute,aktuelleSekunde,locale.atof(Wert[0]), locale.atof(Wert[1]), Differenz, locale.atof(Wert[4]),locale.atof(Wert[5]))
    #DataB.meKursupload(aktuelleWoche,aktuellerTag,aktuelleStunde,aktuelleMinute,aktuelleSekunde,19.88, 19.4, 1.4, 4.0,5.4)
Content.meClose()
