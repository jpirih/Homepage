from site_handlers import BaseHandler

# Kontroler skrito stevilo aplikacija
class SteviloHandler(BaseHandler):
    def get(self):
        return self.render_template("skrito_stevilo.html")

    def post(self):
        vnos_error = "Obvezno vnesi stevilo preden pritisnes gumb!"
        try:
            vneseno_stevilo = int(self.request.get("vnos_stevilo"))
            skrito_stevilo = 25  # najbolj skrito stevilo

            # spremnljivke za parametre
            sporocilo = ""
            bravo = ""

            if vneseno_stevilo == skrito_stevilo:
                bravo = "Bravo uganil si skrito stevilo"
            else:
                sporocilo = "Napaka! Poskusi ponovno "

            params = {"message":sporocilo, "bravo":bravo}
            return self.render_template("skrito_stevilo.html", params=params)
        except ValueError:
            params = {"vnos_err":vnos_error}
            return self.render_template("skrito_stevilo.html", params=params)