# -*- coding: utf-8 -*-
import hashlib
import hmac
import uuid
from google.appengine.ext import ndb

class GuestBook(ndb.Model):
    ime = ndb.StringProperty(default="Neznanec")
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty(required=True)
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)

# Uporabnik za lastni avtentikacijski sistem
# Model uporabnik

class Uporabnik(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    sifrirano_geslo = ndb.StringProperty()

# ustvari  objekt uporabnika in shrani v datastore
    @classmethod
    def ustvari(cls, ime, priimek, email, original_geslo):
        uporabnik = cls(ime=ime, priimek=priimek, email=email, sifrirano_geslo=cls.sifriraj_geslo(original_geslo=original_geslo))
        uporabnik.put()
        return uporabnik

# geslo ki ga uporabnik vnese kot tekst ta funkcvija zakodira tako da je shranjeno geslo sifirirano
    @classmethod
    def sifriraj_geslo(cls, original_geslo):
        salt = uuid.uuid4().hex
        sifra = hmac.new(str(salt), str(original_geslo), hashlib.sha512).hexdigest()
        return "%s:%s" % (sifra, salt)

# funkcija za preverjanje gesla
    @classmethod
    def preveri_geslo(cls, original_geslo, uporabnik):
        sifra, salt = uporabnik.sifrirano_geslo.split(':')
        preverba = hmac.new(str(salt), str(original_geslo), hashlib.sha512).hexdigest()

        if preverba == sifra:
            return True
        else:
            return False

# ---------------- KONEC  Lastnega avtentikacijskegas sitema -----------

# model za sporocila znotraj Kontakt zavihka
class Sporocilo(ndb.Model):
    nastanek = ndb.DateTimeProperty()
    vzdevek = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty()

# ---- USER  model dodatek k google login nekaj dodatnih informacij o uporabniku ---- #

class User(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    vzdevek = ndb.StringProperty(default='vzdevek')
    email = ndb.StringProperty()
    regisriran = ndb.BooleanProperty(default=False)

class MalilMessage(ndb.Model):
    from_email = ndb.StringProperty()
    from_nickname = ndb.StringProperty()
    to_email = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.TextProperty()
    datum = ndb.DateTimeProperty()