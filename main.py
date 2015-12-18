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
from login_sistem.handlers import RegistracijaHandler, LoginHndler


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
    webapp2.Route('/login', LoginHndler, name='login')
], debug=True)





