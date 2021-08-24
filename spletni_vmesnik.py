import bottle
from model import Uporabnik, Zvezek, Stopnja, Program, Vaja

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


#######################################################################
#UPORBANIK


def poisci_racun(zvezek, ime_polja):
    ime_racuna = bottle.request.forms.getunicode(ime_polja)
    return zvezek.poisci_racun(ime_racuna)


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")

def shrani_stanje(uporabnik):
    return uporabnik.v_datoteko()

def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.iz_datoteke(uporabnisko_ime)


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    ime = bottle.request.forms.getunicode("ime")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(ime, uporabnisko_ime, geslo_v_cistopisu)
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

##################################################################################


@bottle.get("/")
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "osnovna_stran.html", zvezek = uporabnik.zvezek, uporabnik = uporabnik)

@bottle.post("/dodaj-stopnjo/")
def dodaj_stopnjo():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    uporabnik.zvezek.dodaj_stopnjo(ime)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.post("/odstrani-stopnjo")
def odstrani_stopnjo():
    pass


@bottle.get("/<ime_stopnje>/")
def ogled_stopnje(ime_stopnje):
    pass



@bottle.post("/dodaj-program")
def dodaj_program(program):
    pass


bottle.run(debug=True, reloader=True)