class Model:
    def __init__(self):
        self.stopnje = []
#        self.razredi = []

    def dodaj_stopnjo(self, stopnja):
        self.stopnje.append(stopnja)

#    def dodaj_razred(self, razred):
#        self.razred.append(razred)

class Vaja:
    def __init__(self, ime, kategorija, program, glasba=None, posnetek=None):
        self.ime = ime
        self.kategorija = kategorija
        self.program = program
        self.glasba = glasba
        self.posnetek = posnetek

class Program:
    def __init__(self, ime, stopnja):
        self.ime = ime
        self.stopnja = stopnja
        self.vaje = []

    def dodaj_vajo(self, vaja):
        self.vaje.append(vaja)

class Stopnja:
    def __init__(self, ime):
        self.ime = ime
        self.programi = []

    def dodaj_program(self, program):
        self.programi.append(program)



#class Razred:
#    def __init__(self, ime, ucitelj):
#        self.ime = ime
#        self.ucitelj = ucitelj
