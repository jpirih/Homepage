from site_handlers import BaseHandler
from models import Uporabnik

# kontrolerji za lasten  login sistem - samo test delovanja
# za ostale pomembne stvari stran uporablja google laogin

# kontroler registracija novega uporabnika
class RegistracijaHandler(BaseHandler):
    def get(self):
        return self.render_template('registracija.html')

    def post(self):
        ime = self.request.get('ime')
        priimek = self.request.get('priimek')
        email = self.request.get('email')
        geslo = self.request.get('geslo')
        ponovno_geslo = self.request.get('ponovno_geslo')

        mail_obstaja = Uporabnik.query(Uporabnik.email == email).fetch()

        if mail_obstaja:
           return self.write('email je ze v bazi')

        elif geslo == ponovno_geslo:
            Uporabnik.ustvari(ime=ime, priimek=priimek, email=email, original_geslo=geslo)
            return self.redirect_to('login')
        else:
            return self.write('Gesli se ne ujemata')


# kontroler za  prijavo uporabnikov
class LoginHndler(BaseHandler):
     def get(self):
         return self.render_template('login.html')

     def post(self):
         try:
             email = self.request.get('email')
             geslo = self.request.get('geslo')
             uporabnik = Uporabnik.query(Uporabnik.email == email).get()
             if Uporabnik.preveri_geslo(original_geslo=geslo, uporabnik=uporabnik):
                self.ustvari_cookie(uporabnik=uporabnik)
                return self.redirect('/login-sistem')
             else:
                 return self.write('Prislo je do napake mail ali geslo ni pravilno ce se nisi se Registriraj :(')
         except:
             return self.write('Prislo je do Napke Pred prvo prijavo je obvezna registracija Pazi na pravilen podatkov')

 # Kontroler zasebne strani test login sistem
class PrijavljenHandler(BaseHandler):
    def get(self):
        return self.render_template('login_correct.html')
