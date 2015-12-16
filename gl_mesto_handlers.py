import csv

#  objekt Glavno mesto

class GlavnoMesto(object):
    ime = "ime glavnega mesta"
    drzava = "drzava glavnega mesta"
    slika = "url slike glavnega mesta"

# konstruktor za objekt glavno mesto
    def __init__(self, ime, drzava, slika):
        self.ime = ime
        self.drzava = drzava
        self.slika = slika


#  funkcija preveri pravilnost vnosa uporabnika
def checkAnswer(city,vnos):
    if vnos == city:
        return True
    else:
        return False

# Funkcija getData prebere podatke iz datoteke ustvari objekte in vrne seznam objektov

def getData(source):
    with open(source,"r") as data:
        content = csv.reader(data)
        list_of_cities = []
        for line in content:
            gl_mesto = GlavnoMesto(ime=line[0], drzava=line[1], slika=line[2])
            list_of_cities.append(gl_mesto)
        return list_of_cities

# ustvari seznam objektov, ki ga uporablja get fukcija znotraj PrestolnicaHandler-ja
# za nakljucno izbiranje mest
seznam = getData("source.txt")





























