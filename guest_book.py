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
            logiran = True
            logout_url = users.create_logout_url('/projects/guest-book')
            params = {'uporabnik': uporabnik, 'logiran': logiran, 'logout_url': logout_url}
        else:
            logiran = False
            login_url = users.create_login_url('/projects/guest-book')
            params = {'uporabnik': uporabnik, 'logiran': logiran, 'login_url': login_url}

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
        seznam = GuestBook.query(GuestBook.izbrisan == False).fetch()
        params = {"seznam":seznam}
        return self.render_template("pregled.html", params=params)

# Kontroler za seznam izbrisanih sporočil
class OznaceniZaBrisanje(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        seznam_izbris = GuestBook.query(GuestBook.izbrisan == True).fetch()

        if uporabnik and uporabnik.nickname() == 'janko.pirih':
            logiran = True
            logout_url = users.create_logout_url('/projects/guest-book/pregled-izbris')
            params ={'uporabnik': uporabnik, 'logiran': logiran, 'logout_url': logout_url, 'seznam_izbris': seznam_izbris}
        else:
            logiran = False
            login_url = users.create_login_url('/projects/guest-book/pregled-izbris')
            params = {'uporabnik': uporabnik, 'logiran': logiran, 'login_url': login_url,'seznam_izbiris': seznam_izbris}

        return self.render_template("seznam_izbris.html", params=params)

# Kontroler za preled posameznega sporocila
class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        # vrne objekt vsa polja ki jih vsebuje sporocilo s dolocenim ID -jem
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {"sporocilo":sporocilo}
        return self.render_template("pregled_posamezno.html", params=params)

# Kontroler za urenanje vnosov
class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporoilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {"sporocilo":sporoilo}
        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        vnos = self.request.get("sporocilo")
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.sporocilo = vnos
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

# Kontroler za brisanje sporocil
class IzbirsiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {"sporocilo":sporocilo}
        return self.render_template("izbris_sporocila.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

# Kontroler za admin delete
class AdminDeleteHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = GuestBook. get_by_id(int(sporocilo_id))

        params = {'sporocilo': sporocilo}
        return self.render_template('admin_delete.html', params=params)

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))

        sporocilo.key.delete()
        return self.redirect_to('seznam-izbirs')

# admin obnovi  sporocilo
class ObnoviSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {'sporocilo': sporocilo}
        return self.render_template('obnovi.html',params=params)

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = False
        sporocilo.put()
        return self.redirect_to('seznam-sporocil')








