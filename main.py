#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import site_handlers
from guest_book.handlers import GuestBookHndler, GuestBookVnosHandler, SeznamVsehVnosovHnadler
from guest_book.handlers import PosameznoSporociloHandler, UrediSporociloHandler, IzbirsiSporociloHandler
from guest_book.handlers import OznaceniZaBrisanje, AdminDeleteHandler, ObnoviSporociloHandler
from skrito_stevilo.handlers import SteviloHandler
from kalkulator.handlers import KalkulatorHandler
from pretvornik.handlers import PretvornikHandler
from forenzik.handlers import ForenzikHandler
from gl_mesto.handlers import PrestolnicaHandler
from login_sistem.handlers import RegistracijaHandler, LoginHndler, PrijavljenHandler
from admin.handlers import AdminHandler, LoginAdminHndler, UrejanjeKontaktSporHandler
from brmail.handlers import PrejetoHandler, PoslanoHandler, NovoSporociloHandler, SporociloPodrnoHandler
from brmail.handlers import OdgovoriHandler, ImenikHandler, SporociloZaUporabnika, BrmailSmetnjakHander



# Route - navigacija po spletnem mestu
app = webapp2.WSGIApplication([
    webapp2.Route('/', site_handlers.MainHandler, name='main'),
    webapp2.Route('/about', site_handlers.AboutHandler),
    webapp2.Route('/blog', site_handlers.BlogHandler),
    webapp2.Route('/activities', site_handlers.ActivitiesHandler),
    webapp2.Route('/contact', site_handlers.ContactHandler),
    webapp2.Route('/projects', site_handlers.ProjectsHandler),
    webapp2.Route('/projects/kalkulator', KalkulatorHandler),
    webapp2.Route('/projects/pretvornik', PretvornikHandler),
    webapp2.Route('/projects/stevilo', SteviloHandler),
    webapp2.Route('/projects/prestolnica',PrestolnicaHandler),
    webapp2.Route('/projects/forenzik', ForenzikHandler),
    webapp2.Route('/projects/guest-book', GuestBookHndler, name="guest-book"),
    webapp2.Route('/projects/guest-book/pregled', GuestBookVnosHandler),
    webapp2.Route('/projects/guest-book/pregled-vseh', SeznamVsehVnosovHnadler, name="seznam-sporocil"),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/uredi',UrediSporociloHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/izbrisi',IzbirsiSporociloHandler),
    webapp2.Route('/projects/guest-book/pregled-izbris',OznaceniZaBrisanje, name='seznam-izbirs'),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/delete', AdminDeleteHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/obnovi', ObnoviSporociloHandler),
    webapp2.Route('/registracija', RegistracijaHandler),
    webapp2.Route('/login', LoginHndler, name='login'),
    webapp2.Route('/login-sistem', PrijavljenHandler),
    webapp2.Route('/prijavi-se', site_handlers.PrijavaHandler, name="prijava"),
    webapp2.Route('/prijavi-se/preveri-mail', site_handlers.PozdravUporabnikHandler),
    webapp2.Route('/prijavi-se/reg-uporabnika', site_handlers.RegUporabnikaHandler, name='reg-uporabnika'),
    webapp2.Route('/admin',AdminHandler, name='admin'),
    webapp2.Route('/admin/kontakt-podrobno/<sporocilo_id:\d+>', UrejanjeKontaktSporHandler),
    webapp2.Route('/admin/login-sistem', LoginAdminHndler),
    webapp2.Route('/projects/brmail/prejeto', PrejetoHandler),
    webapp2.Route('/projects/brmail/poslano', PoslanoHandler, name='brmail-poslano'),
    webapp2.Route('/projects/brmail/novo', NovoSporociloHandler),
    webapp2.Route('/projects/brmail/sporocilo-podrobno/<mail_id:\d+>', SporociloPodrnoHandler),
    webapp2.Route('/projects/brmail/sporocilo/<mail_id:\d+>/odgovori', OdgovoriHandler),
    webapp2.Route('/projects/brmail/imenik', ImenikHandler),
    webapp2.Route('/projects/brmail/sporocilo-za/<user_id:\d+>', SporociloZaUporabnika),
    webapp2.Route('/projects/brmail/smetnjak', BrmailSmetnjakHander, name='brmail-smetnjak'),
], debug=True)





