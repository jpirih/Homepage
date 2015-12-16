
from site_handlers import BaseHandler
from forenzik_logika import*

# Kontroler za aplikacijo Forenzik
class ForenzikHandler(BaseHandler):
    def get(self):

        return self.render_template("forenzik.html")
# funkcija preveri katere lastnosti vsebuje dna - vnesen v obrazec

    def post(self):
        dna = self.request.get("vnos_dna").upper()
        # seznam_vseh_lastnosti import iz forenzik_logika.py
        lastnosti = seznam_vseh_lastnosti

        lastnosti_cloveka = []

        for lastnost in lastnosti:
            if lastnost in dna:
                lastnosti_cloveka.append(lastnosti[lastnost])

        params = {"lastnosti":lastnosti_cloveka}
        return self.render_template("forenzik.html", params=params)