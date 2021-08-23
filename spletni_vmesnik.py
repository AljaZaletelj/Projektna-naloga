import bottle
from model import Uporabnik, Zvezek, Stopnja

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


def poisci_racun(proracun, ime_polja):
    ime_racuna = bottle.request.forms.getunicode(ime_polja)
    return proracun.poisci_racun(ime_racuna)

def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.iz_datoteke(uporabnisko_ime)


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "prijava.html", napaka=e.args[0]
        )

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")



@bottle.get("/")
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html" )

@bottle.get("/zvezek/")
def nacrtovanje_zvezka():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "zvezek.html"
    )

@bottle.get("/programi/")
def programi():
    trenutni_uporabnik()
    return bottle.template("programi.html")


@bottle.post("/dodaj-stopnjo/")
def dodaj_stopnjo():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.query["ime"]
    uporabnik.zvezek.nova_stopnja(ime)
    shrani_stanje(uporabnik)
    bottle.redirect("/")



bottle.run(debug=True, reloader=True)