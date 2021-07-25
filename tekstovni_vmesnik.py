from model import Model, Vaja, Stopnja, Program

edini_model = Model()
prvi_razred = Stopnja("1R")
drugi_razred = Stopnja("2R")
tretji_razred = Stopnja("3R")

dov1 = Program("dov1", drugi_razred)
dov2 = Program("dov2", drugi_razred)

edini_model.dodaj_stopnjo(prvi_razred)
edini_model.dodaj_stopnjo(drugi_razred)
edini_model.dodaj_stopnjo(tretji_razred)

drugi_razred.dodaj_program(dov1)
drugi_razred.dodaj_program(dov2)

plie = Vaja("Plie", "Drog", dov1)
dov1.dodaj_vajo(plie)


###########################################################
# Pomožne funkcije za prikaz
###########################################################


def prikaz_stopnje(stopnja):
    return f"{stopnja.ime}"

def prikaz_programa(program):
    return f"{program.ime}, {program.stopnja}"

###########################################################
# Pomožne funkcije za vnos
###########################################################

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

###########################################################
# Tekstovni vmesnik
###########################################################

def tekstovni_vmesnik():
    uvodni_pozdrav()
    while True:
        osnovni_zaslon()

def uvodni_pozdrav():
    print("Pozdravljen!")

def osnovni_zaslon():
    print("Kaj bi rad počel?")
    print("1) pogledal stopnje")
    print("2) pogledal razrede")
    print("3) dodal vajo")
    print("4)pogledal program")
    vnos = input("> ")
    if vnos == "1":
        pokazi_stopnje()
    elif vnos == "2":
        pass
    elif vnos == "3":
        dodaj_vajo()
    elif vnos == "4":
        prikazi_program()


def pokazi_stopnje():
    for stopnja in edini_model.stopnje:
        print(f"-{stopnja.ime}")

def dodaj_vajo():
    print("V kateri program bi rad dodal vajo?")
    program = input("Vnesi ime programa: ")
    print("V katero kategorijo spada vaja?")
    kategorija = input("Kategorija> ")
    print("Vnesi ime vaje: ")
    ime = input("Ime> ")
    print("Vnesi opis vaje: ")
    opis = input("Opis> ")
    print("Dodaj glasbo: ")
    glasba = input("Glasba> ")
    print("Dodaj posnetek: ")
    posnetek = input("Posnetek> ")
    nova_vaja = Vaja(kategorija, ime, opis, glasba, posnetek)
    program.dodaj_vajo(nova_vaja)

def pokazi_programe():
    print("Izberi stopnjo programa, ki bo si ga rad ogledal:")
    stopnja = input("Stopnja> ") 
    
def prikazi_program():
    print("Izberi stopnjo programa, ki bo si ga rad ogledal:")
    stopnja = input("Stopnja> ")




tekstovni_vmesnik()