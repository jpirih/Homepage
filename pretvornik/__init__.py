from site_handlers import BaseHandler

# Kontroler za pretvornik enot
class PretvornikHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")

    def post(self):
        err_msg = "Pazi v vnosno polje bvezno vnesi stevilo, namesto decimalne veijice uporabi piko ."
        params = {"err":err_msg}
        try:
            number = float(self.request.get("vrednost"))
            pretvorba = self.request.get("nacin_pretvorbe")

            if pretvorba == "m-cm":
                 izracun = number * 100
                 opis = "Pretvorba vrednosti %.2f  metrov  v centimetre znese:" %number
            elif pretvorba == "cm-m":
                 izracun = number *0.01
                 opis = "Pretvorba vrednosti %.2f  centimetrov v metre znese:" %number
            elif pretvorba == "km-milja":
                 izracun = number * 0.621371
                 opis = "Pretvorba vrednosti %.2f  kilometrov v  milje znese:" %number
            elif pretvorba == "h-min":
                izracun = number * 60
                opis = "Pretvorba vrednosti %.2f  ur v  minute znese:" %number
            elif pretvorba == "h-s":
                izracun = number * 3600
                opis = "Pretvorba vrednosti %.2f  ur v  sekunde znese:" %number
            elif pretvorba == "s-h":
                izracun = number *0.000278
                opis = "Pretvorba vrednosti %.2f  s v  ure znese:" %number
            elif pretvorba == "kmh-ms":
                izracun = number * 0.277778
                opis = "Pretvorba vrednosti %.2f  km/h v  m/s znese:" %number

            izracun = round(izracun,2)
            params = {"izracun":izracun, "opis":opis}
            return self.render_template("pretvornik.html", params=params)
        except:
            return self.render_template("pretvornik.html", params=params)