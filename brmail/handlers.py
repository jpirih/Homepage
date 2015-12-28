# brmail Handlers

from site_handlers import BaseHandler
from google.appengine.api import users
from google.appengine.api import mail
from models import MalilMessage, User


class PrejetoHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            sezam_prejtih = MalilMessage.query(uporabnik.email() == MalilMessage.to_email, MalilMessage.izbrisan == False).order(-MalilMessage.datum).fetch()
            params = {'seznam_prejetih': sezam_prejtih, 'uporabnik': uporabnik}
            return self.render_template('brmail_prejeto.html', params=params)
        else:
            return self.redirect_to('prijava')

class PoslanoHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            sezam_poslanih = MalilMessage.query(uporabnik.email() == MalilMessage.from_email, MalilMessage.izbrisan == False).order(-MalilMessage.datum).fetch()
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
                                              subject= 'Prek apliacije Brmail sem ti posal/-a novo sporocilo',
                                              body="Brmail je preprost mail client app razvit v okviru SmartNinja \n"
                                                   "Web Developement1 za prijavo v apliacijo je obvezen google racun\n"
                                                   "aplikacija je dostopna na povezavi \n"
                                                   " http://janko-home-page.appspot.com/projects/brmail/prejeto\n \n"
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

    def post(self, mail_id):
        mail_message = MalilMessage.get_by_id(int(mail_id))
        izbrisan = self.request.get('izbrisan', default_value='no')
        if izbrisan == 'yes':
            mail_message.izbrisan = True
            mail_message.put()
            return self.redirect_to('brmail-smetnjak')
        else:
            return self.write('sporocilo ni za brisat :) ')

class OdgovoriHandler(BaseHandler):
    def get(self, mail_id):
        uporabnik = users.get_current_user()
        if uporabnik:
            mail_message = MalilMessage.get_by_id(int(mail_id))
            params = {'mail_message': mail_message, 'uporabnik': uporabnik}
            return self.render_template('brmail_odgovori.html', params=params)
        else:
            self.redirect_to('prijava')

    def post(self,  mail_id):
        uporabnik = users.get_current_user()
        mail_message = MalilMessage.get_by_id(int(mail_id))

        from_email = self.request.get('from_email')
        to_email = self.request.get('to_email')
        subject = self.request.get('subject')
        odgovor = self.request.get('message')
        datum = self.trenutni_datum_cas()
        from_nickname = uporabnik.nickname()

        mail_message = MalilMessage(from_email=from_email, from_nickname=from_nickname, to_email=to_email,
                                      subject=subject, message=odgovor, datum=datum)

        mail_message.put()
        return self.redirect_to('brmail-poslano')

class ImenikHandler(BaseHandler):
    def get(self):
        seznam_kontaktov = User.query().order(User.priimek).fetch()
        params = {'seznam_kontaktov': seznam_kontaktov}
        return self.render_template('brmail_imenik.html', params=params)

class SporociloZaUporabnika(BaseHandler):
    def get(self, user_id):
        uporabnik = users.get_current_user()
        if uporabnik:
            dolocen_uporabnik = User.get_by_id(int(user_id))
            params = {'uporabnik': uporabnik, 'dolocen_uporabnik':dolocen_uporabnik}
            return self.render_template('brmail_sporocilo_za.html', params=params)
        else:
            self.redirect_to('prijava')

class BrmailSmetnjakHander(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            seznam_izbrisanih = MalilMessage.query(MalilMessage.izbrisan == True,(uporabnik.nickname() == MalilMessage.from_nickname)).fetch()

            params = {'uporabnik': uporabnik, 'seznam_izbrisanih': seznam_izbrisanih}

            return self.render_template('brmail_smetnjak.html', params=params)




