import hashlib
import json
import random


class Zvezek:
    def __init__(self):
        self.stopnje = []
        self.razredi = []


    def nova_stopnja(self, ime_stopnje):
        if ime_stopnje in self._stopnje_po_imenih:
            raise ValueError("Stopnja z tem imenom že obstaja!")
        else:
            nova = Stopnja(ime_stopnje)
            self.stopnje.append(nova)
            self._stopnje_po_imenih[ime_stopnje] = nova
            self._programi_po_imenih[nova] = []

    def odstrani_stopnjo(self, stopnja):
        self._preveri_stopnjo(stopnja)
        for program in stopnja.programi():
            program.stopnja = None
            self._programi_po_stopnjah[None].append(program)
        self.kuverte.remove(stopnja)
        del self._programi_po_stopnjah[stopnja]
    


    def nov_razred(self, ime_razreda):
            if ime_razreda in self._razredi_po_imenih:
                raise ValueError("Razred z tem imenom že obstaja!")
            else:
                nov = Razred(ime_razreda)
                self.razredi.append(nov)
                self._razredi_po_imenih[ime_razreda] = nov

    def odstrani_razred(self, razred):
        self.razredi.remove(razred)



    def v_slovar(self):
        return{
            "stopnje": [
                {
                    "ime stopnje": stopnja.ime,
                    "programi na stopnji": [program.v_slovar() for program in stopnja.programi]
                }
            
                for stopnja in self.stopnje
            ],
            "razredi": [{ "razred" : razred.ime, "ucitelj": razred.ucitelj} for razred in self.razredi]
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        zvezek = cls()
        for stopnja in slovar["stopnje"]:
            nova_stopnja = zvezek.nova_stopnja(
                stopnja["ime"]
            )
        for razred in slovar["stopnje"]:
            nov_razred = zvezek.nov_razred(
                razred["razred"],
                razred["ucitelj"]
            )
        return zvezek


class Stopnja:
    def __init__(self, ime):
        self.ime = ime
        self.programi = []

    def dodaj_program(self, program):
        self.programi.append(program)

    def odstrani_program(self, program):
        self.programi.remove(program)


class Program:
    def __init__(self, ime, stopnja):
        self.ime = ime
        self.stopnja = stopnja
        self.vaje = []

    def dodaj_vajo(self, vaja):
        self.vaje.append(vaja)

    def odstrani_vajo(self, vaja):
        self.vaje.remove(vaja)

    def v_slovar(self):
        return {
            "ime programa": self.ime,
            "stopnja programa": self.stopnja,
            "vaje v programu": [vaja.v_slovar() for vaja in self.vaje] 
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Program(
            slovar["ime programa"],
            slovar["stopnja programa"]
        )


class Vaja:
    def __init__(self, ime, kategorija, program, glasba=None, posnetek=None):
        self.ime = ime
        self.kategorija = kategorija
        self.program = program
        self.glasba = glasba
        self.posnetek = posnetek

    def v_slovar(self):
        return {
            "ime_vaje": self.ime,
            "kategorija": self.kategorija,
            "program": self.program,
            "glasba": self.glasba,
            "posnetek": self.posnetek
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Vaja(
            slovar["ime_vaje"],
            slovar["kategorija"],
            slovar["program"],
            slovar["glasba"],
            slovar["posnetek"]
        )


class Razred:
    def __init__(self, ime, ucitelj):
        self.ime = ime
        self.ucitelj = ucitelj


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, zvezek):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.zvezek = zvezek
#    
#    @staticmethod
#    def prijava(uporabnisko_ime, geslo_v_cistopisu):
#        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
#        if uporabnik is None:
#            raise ValueError("Uporabniško ime ne obstaja")
#        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
#            return uporabnik        
#        else:
#            raise ValueError("Geslo je napačno")
#
#    @staticmethod
#    def registracija(uporabnisko_ime, geslo_v_cistopisu):
#        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
#            raise ValueError("Uporabniško ime že obstaja")
#        else:
#            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
#            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Model())
#            uporabnik.v_datoteko()
#            return uporabnik
#
#    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
#        if sol is None:
#            sol = str(random.getrandbits(32))
#        posoljeno_geslo = sol + geslo_v_cistopisu
#        h = hashlib.blake2b()
#        h.update(posoljeno_geslo.encode(encoding="utf-8"))
#        return f"{sol}${h.hexdigest()}"


#    def preveri_geslo(self, geslo_v_cistopisu):
#        sol, _ = self.zasifrirano_geslo.split("$")
#        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)
#

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "zvezek": self.zvezek.v_slovar(),
        }

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        proracun = Zvezek.iz_slovarja(slovar["proracun"])
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, proracun)


    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    def v_datoteko(self):
        with open(
            Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w"
        ) as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None