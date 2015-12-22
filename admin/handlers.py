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


