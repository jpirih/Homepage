# brmail Handlers

from site_handlers import BaseHandler
from google.appengine.api import users
from google.appengine.api import mail
from models import  MalilMessage


class PrejetoHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            sezam_prejtih = MalilMessage.query(uporabnik.email() == MalilMessage.to_email)
            params = {'seznam_prejetih': sezam_prejtih, 'uporabnik': uporabnik}
            return self.render_template('brmail_prejeto.html', params=params)
        else:
            return self.redirect_to('prijava')

class PoslanoHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            sezam_poslanih = MalilMessage.query(uporabnik.email() == MalilMessage.from_email)
            params = {'seznam_poslanih': sezam_poslanih, 'uporabnik': uporabnik}
            return self.render_template('brmail_poslano.html', params=params)
        else:
            return self.redirect_to('prijava')

class NovoSporociloHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            params = {'uporabnik': uporabnik}
            return self.render_template('brmail_novo_sporocilo.html', params=params)
        else:
            return self.redirect_to('prijava')

    def post(self):
        uporabnik = users.get_current_user()
        from_email = self.request.get('from_email')
        from_nickname = uporabnik.nickname()
        to_email = self.request.get('to_email')
        subject = self.request.get('subject')
        message = self.request.get('message')
        datum = self.trenutni_datum_cas()

        novo_sporocilo = MalilMessage(from_email=from_email, from_nickname=from_nickname, to_email=to_email,
                                      subject=subject, message=message, datum=datum)

        novo_sporocilo.put()
        notification_mail = mail.EmailMessage(sender=from_email, to=to_email,
                                              subject= 'Prek apliacije Brmail sem ti posal/-a novo sporočilo',
                                              body="Brmail je preprost mail client app razvit v okviru SmartNinja \n"
                                                   "Web Developement1 za prijavo v apliacijo je obvezen google racun\n"
                                                   "aplikacija je dostopna na povezavi http://janko-home-page.appspot.com/projects/brmail/prejeto\n"
                                                   " Lep pozdrav %s" % from_nickname)
        notification_mail.send()
        self.redirect_to('brmail-poslano')

class SporociloPodrnoHandler(BaseHandler):
    def get(self, mail_id):
        uporabnlik = users.get_current_user()
        if uporabnlik:
            mail_message = MalilMessage.get_by_id(int(mail_id))
            params={'mail_message': mail_message, 'uporabnik': uporabnlik}
            return self.render_template('brmail_sporocilo_podrobno.html', params=params)
        else:
            return self.redirect_to('prijava')



