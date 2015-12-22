from site_handlers import BaseHandler
from models import Sporocilo
from google.appengine.api import users

# kontroler administracija
class AdminHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik and uporabnik.nickname() == "janko.pirih":
            seznam_sporocil = Sporocilo.query().order(-Sporocilo.nastanek).fetch()
            params = {'seznam': seznam_sporocil, 'uporabnik':uporabnik}
            return self.render_template('admin.html', params=params)
        else:
            self.redirect_to('prijava')