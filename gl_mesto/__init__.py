from site_handlers import BaseHandler
from gl_mesto_handlers import *
import random

# kontroler za aplikacijo  ugani glavno mesto   objekt in funcije so v
# datoteki gl_mesto_handlers.py

class PrestolnicaHandler(BaseHandler):
    def get(self):
        city = random.choice(seznam)
        mesto = city.ime
        drzava = city.drzava
        slika = city.slika

        params ={"mesto":mesto,"drzava":drzava, "img":slika}
        return self.render_template("gl_mesto.html",params=params)

    def post(self):
        vneseno_mesto = self.request.get("vnos_mesto")
        vneseno_mesto = vneseno_mesto.lower()
        izbrano_mesto = self.request.get("mesto")

        # spremenljivke za parametre
        bravo = ""
        napaka = ""

        if checkAnswer(izbrano_mesto,vneseno_mesto):
            bravo = "Res je"
        else:
            napaka = " Napaka !!"

        slika = "/assets/img/kekec.JPG"
        slika_narobe = "/assets/img/klicaj.jpg"
        parametri = {"pravilno":bravo, "narobe":napaka, "img_prav": slika, "img_narobe": slika_narobe}
        return self.render_template("gl_mesto.html", params=parametri)
