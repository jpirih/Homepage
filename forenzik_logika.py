import csv

# funkcija za aplikacijo Forenzik, ki jo krmili Forenzik Handler

# prebere datoteko lastnosti.txt in vrne slovar "dna zapis lastnosti": "ime lastnosti"
def get_lastnosti(lastnosti_file):
    with open(lastnosti_file) as lastnosti_source:
        content = csv.reader(lastnosti_source)
        vse_lastnosti = {}
        for line in content:
            # CCAGCAATCGC: crni lasje
            vse_lastnosti[line[1]] = line[0]
        return vse_lastnosti

# seznam vseh lastnosti vsebuje slovar v obliki  CCAGCAATCGC: crni lasje
seznam_vseh_lastnosti = get_lastnosti("lastnosti.txt")

