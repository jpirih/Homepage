#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import site_handlers
import guest_book
import skrito_stevilo
import kalkulator
import pretvornik
import forenzik
import gl_mesto


# Route - navigacija po spletnem mestu
app = webapp2.WSGIApplication([
    webapp2.Route('/', site_handlers.MainHandler, name='main'),
    webapp2.Route('/about', site_handlers.AboutHandler),
    webapp2.Route('/blog', site_handlers.BlogHandler),
    webapp2.Route('/activities', site_handlers.ActivitiesHandler),
    webapp2.Route('/contact', site_handlers.ContactHandler),
    webapp2.Route('/projects', site_handlers.ProjectsHandler),
    webapp2.Route('/projects/kalkulator', kalkulator.KalkulatorHandler),
    webapp2.Route('/projects/pretvornik', pretvornik.PretvornikHandler),
    webapp2.Route('/projects/stevilo', skrito_stevilo.SteviloHandler),
    webapp2.Route('/projects/prestolnica',gl_mesto.PrestolnicaHandler),
    webapp2.Route('/projects/forenzik', forenzik.ForenzikHandler),
    webapp2.Route('/projects/guest-book', guest_book.GuestBookHndler),
    webapp2.Route('/projects/guest-book/pregled',guest_book.GuestBookVnosHandler),
    webapp2.Route('/projects/guest-book/pregled-vseh',guest_book.SeznamVsehVnosovHnadler, name="seznam-sporocil"),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>',guest_book.PosameznoSporociloHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/uredi',guest_book.UrediSporociloHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/izbrisi',guest_book.IzbirsiSporociloHandler),
    webapp2.Route('/projects/guest-book/pregled-izbris',guest_book.OznaceniZaBrisanje, name='seznam-izbirs'),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/delete',guest_book.AdminDeleteHandler),
    webapp2.Route('/projects/guest-book/sporocilo/<sporocilo_id:\d+>/obnovi',guest_book.ObnoviSporociloHandler),
    webapp2.Route('/registracija', site_handlers.RegistracijaHandler),
    webapp2.Route('/login', site_handlers.LoginHndler, name='login')
], debug=True)





