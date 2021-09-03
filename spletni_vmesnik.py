#from tekstovni_vmesnik import premakni_vajo
import bottle
import os
import shutil
from model import Uporabnik, Zvezek, Vaja, Program

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


def trenutna_stopnja(uporabnik, ime_stopnje):
    for stopnja in uporabnik.zvezek.stopnje:
        if stopnja.ime == ime_stopnje:
            return stopnja
#    return uporabnik.zvezek.najdi_stopnjo_po_imenu(ime_stopnje)

def trenutni_program(uporabnik, ime_programa, ime_stopnje):
    stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    for program in uporabnik.zvezek.programi_na_stopnji(stopnja):
        if program.ime == ime_programa:
            return program
#    return uporabnik.zvezek.najdi_program_iz_stopnje_po_imenu(ime_programa, stopnja)


def trenutna_vaja(uporabnik, ime_vaje, ime_programa, ime_stopnje):
    program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    for vaja in uporabnik.zvezek.vaje_v_programu(program):
        if vaja.ime == ime_vaje:
            return vaja
#    return uporabnik.zvezek.najdi_vajo_iz_programa_po_imenu(ime_vaje, program)

#def unikatno_ime_glasbe(ime_glasbe, ime_vaje, program):
#    unikatno_ime_programa = program.unikatno_ime_programa()
#    return f"glasba {ime_glasbe} za vajo {ime_vaje} iz {unikatno_ime_programa}"
#
#def unikatno_ime_posnetka(ime_posnetka, ime_vaje, program):
#    unikatno_ime_programa = program.unikatno_ime_programa()
#    return f"posnetek {ime_posnetka} za vajo {ime_vaje} iz {unikatno_ime_programa}"


#mape

def ustvari_novo_mapo_za_uporbnika(uporabnisko_ime):
    pot = os.path.join("./views/datoteke", uporabnisko_ime)
    if os.path.isdir(pot):
        pass
    else: 
        os.mkdir(pot)

def ustvari_novo_mapo_za_stopnjo(uporabnik, ime_stopnje):
    uporabnisko_ime = uporabnik.uporabnisko_ime
    skupna_pot = f"./views/datoteke/{uporabnisko_ime}"
    pot = os.path.join(skupna_pot, ime_stopnje)
    if os.path.isdir(pot):
        pass
    else: 
        os.mkdir(pot)

def izbrisi_mapo_za_stopnjo(uporabnik, ime_stopnje):
    pot = os.path.join(f"./views/datoteke/{uporabnik.uporabnisko_ime}", ime_stopnje)
    os.remove(pot)

def ustvari_novo_mapo_za_program(uporabnik, ime_stopnje, ime_programa):
    pot = os.path.join(f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}", ime_programa)
    os.mkdir(pot)

#def izbrisi_mapo_za_program(uporabnik, ime_stopnje, ime_programa):

def ustvari_novo_mapo_za_vajo(uporabnik, ime_stopnje, ime_programa, ime_vaje):
    pot = os.path.join(f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}", ime_vaje)
    if os.path.isdir(pot):
        pass
    else: 
        os.mkdir(pot)
        pot_za_glasbo = os.path.join(pot, "glasba")
        pot_za_posnetke = os.path.join(pot, "posnetki")
        os.mkdir(pot_za_glasbo)
        os.mkdir(pot_za_posnetke)

#def izbrisi_mapo_za_vajo(uporabnik, ime_stopnje, ime_programa, ime_vaje)


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        ustvari_novo_mapo_za_uporbnika(uporabnisko_ime)
        return Uporabnik.iz_datoteke(uporabnisko_ime)
        
    else:
        bottle.redirect("/prijava/")

def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()



#registracija--------------------------------------------------------------------------------------------------------

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

#prijava--------------------------------------------------------------------------------------------------------------

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


#osnovna stran----------------------------------------------------------------------------------------------------------

@bottle.get("/") 
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "osnovna_stran.html", zvezek = uporabnik.zvezek, uporabnik = uporabnik, slika = f"./views/datoteke/slike/tretja_slika.webp")

@bottle.post("/dodaj_stopnjo/")
def dodaj_stopnjo():
    uporabnik = trenutni_uporabnik()
    ime_stopnje = bottle.request.forms["ime_stopnje"]
    ustvari_novo_mapo_za_stopnjo(uporabnik, ime_stopnje)
    uporabnik.zvezek.dodaj_stopnjo(ime_stopnje)
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.post("/odstrani_stopnjo/")
def odstrani_stopnjo():
    uporabnik = trenutni_uporabnik()
    ime_stopnje = bottle.request.forms["ime_stopnje"]
    iskana_stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    uporabnik.zvezek.odstrani_stopnjo(iskana_stopnja)
#    izbrisi_mapo_za_stopnjo(uporabnik, ime_stopnje)
    shrani_stanje(uporabnik)
   
    bottle.redirect("/")


#ogled stopnje-------------------------------------------------------------------------------------------------------

@bottle.get("/stopnja_<ime_stopnje>/")
def ogled_stopnje(ime_stopnje):
    uporabnik = trenutni_uporabnik()
    iskana_stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    return bottle.template("ogled_stopnje.html", stopnja = iskana_stopnja, 
    programi = uporabnik.zvezek.programi_na_stopnji(iskana_stopnja), uporabnik = uporabnik)


@bottle.post("/stopnja_<ime_stopnje>/dodaj-program/")
def dodaj_program(ime_stopnje):
    uporabnik = trenutni_uporabnik()
    iskana_stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    ime_programa = bottle.request.forms["ime_programa"]
    uporabnik.zvezek.dodaj_program(ime_programa, iskana_stopnja)
    ustvari_novo_mapo_za_program(uporabnik, ime_stopnje, ime_programa)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/stopnja_{ime_stopnje}/")


@bottle.post("/stopnja_<ime_stopnje>/odstrani-program/")
def odstrani_program(ime_stopnje):
    uporabnik = trenutni_uporabnik()
    ime_programa = bottle.request.forms["ime_programa"]
    iskan_program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    uporabnik.zvezek.odstrani_program(iskan_program)
    #izbrisi_mapo_za_program(uporabnik, ime_stopnje, ime_programa)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/stopnja_{ime_stopnje}/")


#premakni_program definiraj

#ogled programa---------------------------------------------------------------------------------------------------

@bottle.get("/stopnja_<ime_stopnje>/program_<ime_programa>/")
def ogled_programa(ime_stopnje, ime_programa):
    uporabnik = trenutni_uporabnik()
    iskana_stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    iskan_program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    return bottle.template("ogled_programa.html", uporabnik = uporabnik,  stopnja = iskana_stopnja, program = iskan_program, vaje = uporabnik.zvezek.vaje_v_programu(iskan_program),
    programi_na_stopnji = uporabnik.zvezek.programi_na_stopnji(iskana_stopnja))


@bottle.post("/stopnja_<ime_stopnje>/program_<ime_programa>/dodaj-vajo/")
def dodaj_vajo(ime_stopnje, ime_programa):
    uporabnik = trenutni_uporabnik()
    iskan_program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    ime_vaje = bottle.request.forms["ime_vaje"]
    ustvari_novo_mapo_za_vajo(uporabnik, ime_stopnje, ime_programa, ime_vaje)
    kategorija = bottle.request.forms["kategorija"]
    opis = bottle.request.forms["opis"]
    #nalozi glasbo
    glasba = bottle.request.files.get("glasba")
    ime_glasbe = glasba.filename
    #_, ext = os.path.splitext(glasba.filename)
    #if ext not in ('.wav','.mp3'):
    #    return 'File extension not allowed.'
    shrani_v = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}/{ime_vaje}/glasba"
    glasba.save(shrani_v)
    #nalozi posnetek
    posnetek = bottle.request.files.get("posnetek")
    ime_posnetka = posnetek.filename
    #_, ext = os.path.splitext(posnetek.filename)
    #if ext not in ('.wav','.mp4'):
    #    return 'File extension not allowed.'
    shrani_v = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}/{ime_vaje}/posnetki"
    posnetek.save(shrani_v)
    uporabnik.zvezek.dodaj_vajo(ime_vaje, iskan_program, kategorija, opis, ime_glasbe, ime_posnetka)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/stopnja_{ime_stopnje}/program_{ime_programa}/")


@bottle.post("/stopnja_<ime_stopnje>/program_<ime_programa>/odstrani-vajo/")
def odstrani_vajo(ime_stopnje, ime_programa):
    uporabnik = trenutni_uporabnik()
    ime_vaje = bottle.request.forms["ime_vaje"]
    iskan_program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    for vaja in uporabnik.zvezek.vaje:
        if vaja.ime == ime_vaje and vaja.program == iskan_program:
            iskana_vaja = vaja
    uporabnik.zvezek.odstrani_vajo(iskana_vaja)
    #izbrisi_mapo_za_vajo(uporabnik, ime_stopnje, ime_programa, ime_vaje)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/stopnja_{ime_stopnje}/program_{ime_programa}/")


@bottle.post("/stopnja_<ime_stopnje>/program_<ime_programa>/premakni-vajo/")
def premanki_vajo(ime_stopnje, ime_programa):
    uporabnik = trenutni_uporabnik()
    ime_vaje = bottle.request.forms["vaja"]
    iskana_vaja = trenutna_vaja(uporabnik, ime_vaje, ime_programa, ime_stopnje)
    ime_v_program = bottle.request.forms["ime_v_program"]
    v_program = trenutni_program(uporabnik, ime_v_program, ime_stopnje)
    iskana_vaja.premakni_vajo(v_program)
    #premakni mapo
    source = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}/{ime_vaje}"
    destination = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_v_program}"
    shutil.move(source, destination)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/stopnja_{ime_stopnje}/program_{ime_programa}/")


#ogled vaje---------------------------------------------------------------------------------------------------

@bottle.get("/stopnja_<ime_stopnje>/program_<ime_programa>/vaja_<ime_vaje>/")
def ogled_vaje(ime_stopnje, ime_programa, ime_vaje):
    uporabnik = trenutni_uporabnik()
    iskana_stopnja = trenutna_stopnja(uporabnik, ime_stopnje)
    iskan_program = trenutni_program(uporabnik, ime_programa, ime_stopnje)
    iskana_vaja = trenutna_vaja(uporabnik, ime_vaje, ime_programa, ime_stopnje)
    return bottle.template("ogled_vaje.html", uporabnik = uporabnik, stopnja = iskana_stopnja, program = iskan_program, vaja = iskana_vaja,
    posnetek = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}/{ime_vaje}/posnetki", glasba = f"./views/datoteke/{uporabnik.uporabnisko_ime}/{ime_stopnje}/{ime_programa}/{ime_vaje}/glasba")

# pomoc --------------------------------------------------------------------------------------------------------
@bottle.get("/pomoc/")
def pomoc():
    return bottle.template("pomoc.html")


if __name__ == "__main__":
    bottle.run(debug=True, reloader=True)