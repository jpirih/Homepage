from site_handlers import BaseHandler
from models import Sporocilo, Uporabnik
from google.appengine.api import users

# kontroler administracija
class AdminHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            seznam_sporocil = Sporocilo.query().order(-Sporocilo.nastanek).fetch()
            params = {'seznam': seznam_sporocil, 'uporabnik':uporabnik}
            return self.render_template('admin.html', params=params)
        else:
            self.redirect_to('prijava')

# pregled uporabnikov login-sistema
class LoginAdminHndler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()

        if uporabnik:
            seznam = Uporabnik.query().order(Uporabnik.priimek).fetch()
            params = {'seznam': seznam,'uporabnik': uporabnik}
            return self.render_template('admin_login_sistem.html', params=params)
        else:
            self.redirect_to('prijava')

# podrobnosti kontaktnih sporocil

class UrejanjeKontaktSporHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()
        if uporabnik:
            pos_sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
            params = {'uporabnik': uporabnik, 'sporocilo': pos_sporocilo}
            return  self.render_template('sporocilo_podrobno.html', params=params)
        else:
            return self.redirect_to('prijava')


