from model import Zvezek, Vaja, Stopnja, Program

DATOTEKA_S_STANJEM = "stanje.json"

try:
    zvezek = Zvezek.nalozi_stanje(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    zvezek = Zvezek()



# Pomožne funkcije za prikaz

def prikaz_stopnje(stopnja):
    return f"{stopnja.ime}"

def prikaz_programa(program):
    return f"{program.ime} za {program.stopnja}"

def prikaz_vaje(vaja):
    return f"{vaja.ime} iz {vaja.program}: {vaja.kategorija}, {vaja.opis}, {vaja.glasba}, {vaja.posnetek}"

# Pomožne funkcije za vnos

def vnesi_stevilo(pozdrav):
    """S standardnega vhoda prebere naravno število."""
    while True:
        try:
            vnos = input(pozdrav)
            return int(vnos)
        except ValueError:
            print("Prosim, da vnesete število!")

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
            print("Kaj bi radi naredili?")
            moznosti = [
                ("pogledal stopnje", pokazi_stopnje),
                ("pogledal razrede", pokazi_stopnje),
                ("dodal vajo", dodaj_vajo),
                ("odstranil_vajo", odstrani_vajo),
                ("pogledal program", prikazi_program),
                ("pogledal seznam programov", pokazi_programe)
            ]
            izbira = izberi(moznosti)
            izbira()
            print()
            input("Pritisnite ENTER za shranjevanje in vrnitev v osnovni meni...")
            zvezek.shrani(DATOTEKA_S_STANJEM)
        except ValueError as e:
            print(e.args[0])
        except KeyboardInterrupt:
            print()
            print("Nasvidenje!")
            return

def uvodni_pozdrav():
    print("Pozdravljen!")
    print("Za izhod pritisnite tipko Ctrl-C.")


def pokazi_stopnje():
    for stopnja in zvezek.stopnje:
        print(f"-{stopnja.ime}")

def dodaj_vajo():
    print("Izberi stopnjo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("V kateri program bi rad dodal vajo?")
    program = izberi_program(stopnja.programi)
    print("V katero kategorijo spada vaja?")
    kategorija = input("Kategorija> ")
    print("Vnesi ime vaje: ")
    ime = input("Ime> ")
    #print("Dodaj glasbo: ")
    #glasba = input("Glasba> ")
    #print("Dodaj posnetek: ")
    #posnetek = input("Posnetek> ")
    nova_vaja = Vaja(ime, kategorija, program)
    zvezek.dodaj_vajo(nova_vaja)
    print(f"Vaja {ime} je uspešno dodana.")

def odstrani_vajo():
    print("Izberi stopnjo iz katere bi rad izbrisal vajo:")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    print("Iz katerega programa bi rad izbrisal vajo?")
    program = izberi_program(stopnja.programi)
    print("Izberi vajo, ki bi jo rad izbrisal:")
    vaja = izberi_vajo(program.vaje)
    if (input(f"Ste prepričani, da želite odstaniti vajo {vaja.ime}? [da/NE]") == "da"):
        program.odstrani_vajo(vaja)
        print("Vaja je uspešno odstanjena!")
    else:
        ("Odstranitev vaje je preklicana.")

def pokazi_programe():
    print("Izberi stopnjo programa, ki bo si ga rad ogledal: ")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    for program in stopnja.programi:
        print(f"-{program.ime}")
    
def prikazi_program():
    print("Izberi stopnjo programa, ki bo si ga rad ogledal: ")
    stopnja = izberi_stopnjo(zvezek.stopnje)
    for program in stopnja.programi:
        print(f"-{program.ime}")
    print("Izberi program, ki bi si ga rad ogledal:")
    program = izberi_program(stopnja.programi)
    for vaja in program.vaje:
        print(f"-{vaja.ime}, {vaja.kategorija}")



tekstovni_vmesnik()