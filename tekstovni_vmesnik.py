from model import Zvezek, Program, Vaja

DATOTEKA_S_STANJEM = "stanje.json"

try:
    zvezek = Zvezek.nalozi_stanje(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    zvezek = Zvezek()


# Pomožne funkcije za prikaz

def prikaz_stopnje(stopnja):
    return f"{stopnja.ime}"


def prikaz_programa(program):
    return f"{program.ime} na {program.stopnja.ime}"


def prikaz_vaje(vaja):
    return f"{vaja.ime}: {vaja.kategorija}, {vaja.opis}, {vaja.glasba}, {vaja.posnetek}"

# Pomožne funkcije za vnos


def vnesi_stevilo(pozdrav):
    """S standardnega vhoda prebere naravno število."""
    while True:
        try:
            stevilo = input(pozdrav)
            return int(stevilo)
        except ValueError:
            print("Prosim, da vnesete število!")

#


def izberi(seznam):
    if len(seznam) == 1:
        opis, element = seznam[0]
        print(f"Na voljo je samo možnost {opis}, zato sem jo izbral.")
        return element
    for indeks, (oznaka, _) in enumerate(seznam, 1):
        print(f"{indeks}) {oznaka}")
    while True:
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(f"Izberi število med 1 in {len(seznam)}")


def izberi_stopnjo(stopnje):
    return izberi([(prikaz_stopnje(stopnja), stopnja) for stopnja in stopnje])


def izberi_program(programi):
    return izberi([(prikaz_programa(program), program) for program in programi])


def izberi_vajo(vaje):
    return izberi([(prikaz_vaje(vaja), vaja) for vaja in vaje])


# Tekstovni vmesnik


def tekstovni_vmesnik():
    uvodni_pozdrav()
    while True:
        try:
            moznosti = [
                ("pogledal stopnje", pokazi_stopnje),
                ("dodal stopnjo", dodaj_stopnjo),
                ("odstranil stopnjo", odstrani_stopnjo),
                ("pogledal programe na stopnji", pokazi_programe_na_stopnji),
                ("dodal program", dodaj_program),
                ("odstranil program", odstrani_program),
                ("pogledal vaje v programu", pokazi_vaje_v_programu),
                ("pogledal kategorije v programu", pokazi_kategorije_v_programu),
                ("dodal vajo", dodaj_vajo),
                ("odstranil_vajo", odstrani_vajo),
                ("premaknil vajo", premakni_vajo),
                ("uredil vajo", uredi_vajo)
            ]
            print(20 * "-")
            print("Kaj bi radi naredili?")
            izbira = izberi(moznosti)
            izbira()
            print("Shranjujem...")
            zvezek.shrani_stanje(DATOTEKA_S_STANJEM)
            print("Shranjeno!")
        except ValueError as e:
            print(e.args[0])
        except KeyboardInterrupt:
            print("Nasvidenje!")
            return


def uvodni_pozdrav():
    print("Pozdravljen!")
    print("Za izhod pritisnite tipko Ctrl-C.")


def pokazi_stopnje():
    if len(zvezek.stopnje) == 0:
        print("Trenutno nimaš še nobenih stopenj!")
    else:
        for stopnja in zvezek.stopnje:
            print(prikaz_stopnje(stopnja))


def dodaj_stopnjo():
    print("Vnesi ime stopnje:")
    ime = input("Ime stopnje: ")
    zvezek.dodaj_stopnjo(ime)
    print(f"Stopnja {ime} je uspešno dodana!")


def odstrani_stopnjo():
    print("Katero stopnjo bi rad odstranil?")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    if (input(f"Ste prepričani, da želite odstaniti stopnjo {stopnja.ime}? [da/NE] ") == "da"):
        zvezek.odstrani_stopnjo(stopnja)
        print("Vaja je uspešno odstanjena!")
    else:
        print("Odstranitev stopnje je preklicana.")


def pokazi_programe_na_stopnji():
    print("Izberi stopnjo za katero bi si rad ogledal programe:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    if len(zvezek.programi_na_stopnji(stopnja)) == 0:
        print("Na tej stopnji nimaš še nobenih programov!")
    else:
        for program in zvezek.programi_na_stopnji(stopnja):
            print(prikaz_programa(program))


def dodaj_program():
    print("Za katero stopnjo bi rad dodal program?")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Vnesi ime programa:")
    ime = input("> ")
    zvezek.dodaj_program(ime, stopnja)


def odstrani_program():
    print("Program za katero stopnjo bi rad odstranil?")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Izberi program ki bi ga rad odstanil:")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    if (input(f"Ste prepričani, da želite odstaniti program {program.ime}? [da/NE]") == "da"):
        zvezek.odstrani_program(program)
        print("Program je uspešno odstanjen!")
    else:
        print("Odstranitev programa je preklicana.")


def pokazi_vaje_v_programu():
    print("Izberi stopnjo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Izberi program katerega vaje bi si rad ogledal:")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    if len(zvezek.vaje_v_programu(program)) == 0:
        print("V tem programu nimaš še nobenih vaj!")
    else:
        for vaja in zvezek.vaje_v_programu(program):
            print(prikaz_vaje(vaja))


def pokazi_kategorije_v_programu():
    print("Izberi stopnjo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Izberi program katerega kategorije bi si rad ogledal:")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    kategorije = zvezek.kategorije_v_programu(program)
    if kategorije == []:
        print("V tem programu nimaš nobenih kategorij!")
    else:
        for kategorija in kategorije:
            print(kategorija)


def dodaj_vajo():
    print("Izberi stopnjo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("V kateri program bi rad dodal vajo?")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    print("V katero kategorijo spada vaja?")
    kategorija = input("Kategorija> ")
    print("Vnesi ime vaje: ")
    ime = input("Ime> ")
    print("Dodaj opis vaje:")
    opis = input("> ")
    print("Dodaj glasbo: ")
    glasba = input("Glasba> ")
    print("Dodaj posnetek: ")
    posnetek = input("Posnetek> ")
    zvezek.dodaj_vajo(ime, program, kategorija, opis, glasba, posnetek)
    print(f"Vaja {ime} je uspešno dodana.")


def odstrani_vajo():
    print("Izberi stopnjo iz katere bi rad izbrisal vajo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Iz katerega programa bi rad izbrisal vajo?")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    print("Izberi vajo, ki bi jo rad izbrisal:")
    vaja = izberi_vajo(zvezek.vaje_v_programu(program))
    if (input(f"Ste prepričani, da želite odstaniti vajo {vaja.ime}? [da/NE]") == "da"):
        zvezek.odstrani_vajo(vaja)
        print("Vaja je uspešno odstanjena!")
    else:
        print("Odstranitev vaje je preklicana.")


def premakni_vajo():
    print("Izberi stopnjo na kateri bi rad premaknil vajo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Iz katerega programa bi rad premaknil vajo?")
    prvi_program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    print("Katero vajo bi rad premaknil?")
    vaja = izberi_vajo(zvezek.vaje_v_programu(prvi_program))
    print("V kateri program bi rad prestavil vajo?")
    drugi_program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    vaja.program = drugi_program
    print("Vaja je uspešno premaknjena!")


def uredi_vajo():
    print("Izberi stopnjo na kateie bi rad uredil vajo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Iz katerega programa bi rad uredil vajo?")
    program = izberi_program(zvezek.programi_na_stopnji(stopnja))
    print("Izberi vajo, ki bi jo rad uredil:")
    vaja = izberi_vajo(zvezek.vaje_v_programu(program))
    print("Dodaj novo ime vaje:")
    print("Če kategorije ne želiš spremeniti pusti polje prazno.")
    novo_ime = input("Novo ime: ")
    print("V katero kategorijo bi rad prestavil vajo?")
    print("Če kategorije ne želiš spremeniti pusti polje prazno.")
    nova_kategorija = input("Nova kategorija: ")
    print("Dodaj nov opis vaje.")
    print("Če opisa ne želiš spremeniti pusti polje prazno.")
    nov_opis = input("Nov opis: ")
    print(novo_ime)
    vaja.ime = novo_ime
    print(novo_ime)
    vaja.spremeni_kategorijo(nova_kategorija)
    vaja.spremeni_opis(nov_opis)
    print("Vaja je spremenjena!")


if __name__ == "__main__":
    tekstovni_vmesnik()
