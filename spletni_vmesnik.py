import bottle
from model import Uporabnik, Zvezek

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


#######################################################################
#UPORBANIK

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
    if uporabnisko_ime:
        return Uporabnik.iz_datoteke(uporabnisko_ime)

    else:
        bottle.redirect("/prijava/")

def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


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

@bottle.post("/dodaj_stopnjo/")
def dodaj_stopnjo():
    uporabnik = trenutni_uporabnik()
    ime_stopnje = bottle.request.forms["ime_stopnje"]
    uporabnik.zvezek.dodaj_stopnjo(ime_stopnje)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.post("/odstrani_stopnjo/")
def odstrani_stopnjo():
    pass


@bottle.get("/<ime_stopnje>/")
def ogled_stopnje(ime_stopnje):
    uporabnik = trenutni_uporabnik()
    for stopnja in uporabnik.zvezek.stopnje:
        if stopnja.ime == ime_stopnje:
            trenutna_stopnja = stopnja
    return bottle.template("ogled_stopnje.html", stopnja = trenutna_stopnja, programi = uporabnik.zvezek.programi_na_stopnji(trenutna_stopnja))


@bottle.post("/<ime_stopnje>/dodaj-program/")
def dodaj_program(ime_stopnje):
    uporabnik = trenutni_uporabnik()
    for stopnja in uporabnik.zvezek.stopnje:
        if stopnja.ime == ime_stopnje:
            trenutna_stopnja = stopnja
    ime = bottle.request.forms["ime_programa"]
    uporabnik.dodaj_program(ime, stopnja)


@bottle.post("/odstrani-prorgam/")
def odstrani_program(program):
    pass


#premakni_program
#
#ogled_programa
#
#dodaj_vajo
#
#odstrani_vajo
#
#premakni_vajo
#
#uredi_vajo


@bottle.get("/pomoc/")
def pomoc():
    return bottle.template("pomoc.html")


bottle.run(debug=True, reloader=True)