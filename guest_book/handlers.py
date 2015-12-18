#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import GuestBook
from google.appengine.api import users
from site_handlers import BaseHandler

# -------------- KNJIGA GOSTOV ------------

# Kontroler za GuestBook aplikacijo
class GuestBookHndler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            prijavljen = True
            logout_url = users.create_logout_url('/projects/guest-book')
            params = {'uporabnik': uporabnik, 'prijavljen': prijavljen, 'logout_url': logout_url}
        else:
            prijavljen = False
            login_url = users.create_login_url('/projects/guest-book')
            params = {'uporabnik': uporabnik, 'prijavljen': prijavljen, 'login_url': login_url}

        return self.render_template("guest_book.html", params=params)

# Pregled vnesenih podatkov in shranjevanje v Bazo
class GuestBookVnosHandler(BaseHandler):
    err = ""
    def post(self):
        ime = self.request.get("ime")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        msg = GuestBook(ime=ime, email=email, sporocilo=sporocilo)
        params = {'msg': msg}

        if msg.ime == "":
            msg.ime = "Neznanec"
            msg.put()
            return self.render_template("vnos.html", params=params)
        elif msg.sporocilo == "" or msg.sporocilo[0] == " ":
            msg.sporocilo = "privzeto besedilo - uporabnik ni vpisal teksta"
            msg.put()
            return self.render_template("vnos.html", params=params)
        else:
            msg.put()
            return self.render_template("vnos.html", params=params)


# Kontroler seznam vnosov
class SeznamVsehVnosovHnadler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            seznam = GuestBook.query(GuestBook.izbrisan == False).fetch()
            params = {"seznam":seznam}
            return self.render_template("pregled.html", params=params)
        else:
            return self.redirect_to('guest-book')

# Kontroler za seznam izbrisanih sporočil
class OznaceniZaBrisanje(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        seznam_izbris = GuestBook.query(GuestBook.izbrisan == True).fetch()

        if uporabnik and uporabnik.nickname() == 'janko.pirih':
            prijavljen = True
            logout_url = users.create_logout_url('/projects/guest-book/pregled-izbris')
            params ={'uporabnik': uporabnik, 'prijavljen': prijavljen, 'logout_url': logout_url, 'seznam_izbris': seznam_izbris}
        else:
            prijavljen = False
            login_url = users.create_login_url('/projects/guest-book/pregled-izbris')
            params = {'uporabnik': uporabnik, 'logiran': prijavljen, 'login_url': login_url,'seznam_izbiris': seznam_izbris}

        return self.render_template("seznam_izbris.html", params=params)

# Kontroler za preled posameznega sporocila
class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()
        if uporabnik:
            # vrne objekt vsa polja ki jih vsebuje sporocilo s dolocenim ID -jem
            sporocilo = GuestBook.get_by_id(int(sporocilo_id))
            params = {"sporocilo":sporocilo}
            return self.render_template("pregled_posamezno.html", params=params)
        else:
            return self.redirect_to('guest-book')

# Kontroler za urenanje vnosov
class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()
        if uporabnik:
            sporoilo = GuestBook.get_by_id(int(sporocilo_id))
            params = {"sporocilo":sporoilo}
            return self.render_template("uredi_sporocilo.html", params=params)
        else:
            return self.redirect_to('guest-book')


    def post(self, sporocilo_id):
        vnos = self.request.get("sporocilo")
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.sporocilo = vnos
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

# Kontroler za brisanje sporocil
class IzbirsiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()

        if uporabnik:
            sporocilo = GuestBook.get_by_id(int(sporocilo_id))
            params = {"sporocilo":sporocilo}
            return self.render_template("izbris_sporocila.html", params=params)
        else:
            return self.redirect_to('guest-book')

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

# Kontroler za admin delete
class AdminDeleteHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()

        if uporabnik.nickname() == 'janko.pirih':
            sporocilo = GuestBook. get_by_id(int(sporocilo_id))

            params = {'sporocilo': sporocilo}
            return self.render_template('admin_delete.html', params=params)
        else:
            return self.redirect_to('seznam-izbiris')

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))

        sporocilo.key.delete()
        return self.redirect_to('seznam-izbirs')

# admin obnovi  sporocilo
class ObnoviSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        uporabnik = users.get_current_user()

        if uporabnik.nickname() == 'janko.pirih':
            sporocilo = GuestBook.get_by_id(int(sporocilo_id))
            params = {'sporocilo': sporocilo}
            return self.render_template('obnovi.html',params=params)
        else:
            return self.redirect_to('seznam-izbirs')

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = False
        sporocilo.put()
        return self.redirect_to('seznam-sporocil')








