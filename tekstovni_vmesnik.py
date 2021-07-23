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
    vnos = input("> ")
    if vnos == "1":
        pokazi_stopnje()
    elif vnos == "2":
        pass

def pokazi_stopnje():
    for stopnja in edini_model.stopnje:
        print(f"-{stopnja.ime}")


tekstovni_vmesnik()