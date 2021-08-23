import hashlib
import json
import random


class Zvezek:
    def __init__(self):
        self.stopnje = []
        self.programi = []
        self.vaje = []


    def dodaj_stopnjo(self, ime_stopnje):
        nova = Stopnja(ime_stopnje)
        self.stopnje.append(nova)

    def odstrani_stopnjo(self, stopnja):
        self.stopnje.remove(stopnja)


    def dodaj_program(self, ime, stopnja):
        nov = Program(ime, stopnja)
        self.programi.append(nov)

    def odstrani_program(self, program):
        self.programi.remove(program)


    def dodaj_vajo(self, ime, program, kategorija, opis="", glasba=None, posnetek=None):
        nova = Vaja(ime, program, kategorija, opis, glasba, posnetek)
        self.vaje.append(nova)

    def odstrani_vajo(self, vaja):
        self.vaje.remove(vaja)



    def v_slovar(self):
        return {
            "stopnje": [
                {
                    "ime_stopnje": stopnja.ime,
                }
                for stopnja in self.stopnje
            ],
            "programi": [
                {
                    "ime_programa" : program.ime,
                    "stopnja_programa": program.stopnja,
                }
                for program in self.programi
            ],
            "vaje": [
                {
                    "ime_vaje": vaja.ime,
                    "iz_programa": vaja.program,
                    "kategorija_vaje": vaja.kategorija,
                    "opis": vaja.opis,
                    "glasba": vaja.glasba,
                    "posnetek": vaja.posnetek
                }
                for vaja in self.vaje
            ],
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        zvezek = cls()
        for stopnja in slovar["stopnje"]:
            zvezek.dodaj_stopnjo(stopnja["ime_stopnje"])
        for program in slovar["programi"]:
            zvezek.dodaj_program(program["ime_programa"], program["stopnja_programa"])
        for vaja in slovar["vaje"]:
            zvezek.dodaj_vajo(
                vaja["ime_vaje"],
                vaja["iz_programa"],
                vaja["kategorija_vaje"],
                vaja["opis"],
                vaja["glasba"],
                vaja["posnetek"]
            )
        return zvezek


    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, "w") as datoteka:
            json.dump(self.slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
        return cls.iz_slovarja(slovar)








class Stopnja:
    def __init__(self, ime, zvezek):
        self.ime = ime
        self.zvezek = zvezek



class Program:
    def __init__(self, ime, stopnja, zvezek):
        self.ime = ime
        self.stopnja = stopnja
        self.zvezek = zvezek


class Vaja:

    def __init__(self, ime, program, kategorija, opis="", glasba=None, posnetek=None):
        self.ime = ime
        self.program = program
        self.kategorija = kategorija
        self.opis = opis
        self.glasba = glasba
        self.posnetek = posnetek



#############################################################################
#UPORABNIK



class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, zvezek):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.zvezek = zvezek

    #prijava
    
    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik        
        else:
            raise ValueError("Geslo je napačno")


    
    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None


    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)


    #registracija

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Zvezek())
            uporabnik.v_datoteko()
            return uporabnik


    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"


    def v_datoteko(self):
        with open(
            Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w", encoding="utf-8"
        ) as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    #slovar

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "zvezek": self.zvezek.v_slovar()
        }

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        zvezek = Zvezek.iz_slovarja(slovar["zvezek"])
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, zvezek)




