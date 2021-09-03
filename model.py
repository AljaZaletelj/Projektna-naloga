import hashlib
import json
import random

#UPORABNIK: ime, up.ime, geslo, zvezek
#ZVEZEK: stopnje, programi, vaje
#STOPNJA: ime
#PROGRAM: ime, stopnja
#VAJA: ime, program, kategorija, opis, glasba, posnetek

#Zvezek--------------------------------------------------------------------------------------------------------------

class Zvezek:
    def __init__(self):
        self.stopnje = []
        self.programi = []
        self.vaje = []


    def dodaj_stopnjo(self, ime_stopnje):
        for stopnja in self.stopnje:
            if stopnja.ime == ime_stopnje:
                raise ValueError("Stopnja s tem imenom že obstaja!")
        nova = Stopnja(ime_stopnje)
        self.stopnje.append(nova)

    def odstrani_stopnjo(self, stopnja):
        self.stopnje.remove(stopnja)

    #dodajanje in odstranjevanje

    def dodaj_program(self, ime, stopnja):
  #      for program in self.programi_na_stopnji(stopnja):
  #          if program.ime == ime:
  #              raise ValueError("Program s tem imenom na tej stopnji že obstaja!")
        nov = Program(ime, stopnja)
        self.programi.append(nov)

    def odstrani_program(self, program):
        self.programi.remove(program)


    def dodaj_vajo(self, ime, program, kategorija, opis="", glasba=None, posnetek=None):
 #       for vaja in self.vaje_v_programu(program):
 #           if vaja.ime == ime:
 #               raise ValueError("Vaja s tem imenom v tem programu že obstaja!")
        nova = Vaja(ime, program, kategorija, opis, glasba, posnetek)
        self.vaje.append(nova)

    def odstrani_vajo(self, vaja):
        self.vaje.remove(vaja)




    #kupckanje

    def programi_na_stopnji(self, stopnja):
        programi_na_stopnji = []
        for program in self.programi:
            if program.stopnja == stopnja:
                programi_na_stopnji.append(program)
        return programi_na_stopnji

    def vaje_v_programu(self, program):
        vaje_v_programu = []
        for vaja in self.vaje:
            if vaja.program == program:
                vaje_v_programu.append(vaja)
        return vaje_v_programu



    #iskanje

    def najdi_stopnjo_po_imenu(self, ime_stopnje):
        for stopnja in self.stopnje:
            if stopnja.ime == ime_stopnje:
                return stopnja


    def najdi_program_iz_stopnje_po_imenu(self, ime_programa, stopnja):
        unikatno_ime = f"{ime_programa} za {stopnja.ime}"
        for program in self.programi:
            if program.unikatno_ime_programa() == unikatno_ime:
                return program

    def najdi_vajo_iz_programa_po_imenu(self, ime_vaje, program):
        unikatno_ime = f"{ime_vaje} v {program.ime} za {program.stopnja.ime}"
        for vaja in self.vaje:
            if vaja.unikatno_ime_vaje() == unikatno_ime:
                return vaja


    #zapisovanje v json

    def v_slovar(self):
        return {
            "stopnje": [
                {
                    "ime_stopnje" : stopnja.ime
                }
                for stopnja in self.stopnje
            ],
            "programi": [
                {
                    "ime_programa" : program.ime,
                    "ime_stopnje" : program.stopnja.ime
                }
                for program in self.programi
            ],
            "vaje": [
                {
                    "ime_vaje" : vaja.ime,
                    "ime_programa": vaja.program.ime,
                    "ime_stopnje" : vaja.program.stopnja.ime,
                    "kategorija_vaje" : vaja.kategorija,
                    "opis": vaja.opis,
                    "glasba" : vaja.glasba,
                    "posnetek": vaja.posnetek
                }
                for vaja in self.vaje
            ],
        }

    @classmethod
    def iz_slovarja(cls, slovar_s_stanjem):
        zvezek = cls()
        for stopnja in slovar_s_stanjem["stopnje"]:
            zvezek.dodaj_stopnjo(stopnja["ime_stopnje"])
        for program in slovar_s_stanjem["programi"]:
            stopnja = zvezek.najdi_stopnjo_po_imenu(program["ime_stopnje"])
            zvezek.dodaj_program(program["ime_programa"], stopnja)
        for vaja in slovar_s_stanjem["vaje"]:
            stopnja = zvezek.najdi_stopnjo_po_imenu(vaja["ime_stopnje"])
            program = zvezek.najdi_program_iz_stopnje_po_imenu(vaja["ime_programa"], stopnja)
            zvezek.dodaj_vajo(
                vaja["ime_vaje"],
                program,
                vaja["kategorija_vaje"],
                vaja["opis"],
                vaja["glasba"],
                vaja["posnetek"]
            )
        return zvezek


    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, "w", encoding="utf-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_stanjem = json.load(datoteka)
        return cls.iz_slovarja(slovar_s_stanjem)


#Stopnja, Program, Vaja -------------------------------------------------------------------------------
 
class Stopnja:
    def __init__(self, ime):
        self.ime = ime


class Program:
    def __init__(self, ime, stopnja):
        self.ime = ime
        self.stopnja = stopnja

    def unikatno_ime_programa(self):
        return f"{self.ime} za {self.stopnja.ime}"

class Vaja:

    def __init__(self, ime, program, kategorija, opis="", glasba=None, posnetek=None):
        self.ime = ime
        self.program = program
        self.kategorija = kategorija
        self.opis = opis
        self.glasba = glasba
        self.posnetek = posnetek

    def unikatno_ime_vaje(self):
        return f"{self.ime} v {self.program.ime} za {self.program.stopnja.ime}"

    def unikatno_ime_glasbe(self, ime_glasbe):
        unikatno_ime_vaje = self.unikatno_ime_vaje
        return f"glasba {ime_glasbe} za {unikatno_ime_vaje}"


    def unikatno_ime_posnetka(self, ime_posnetka):
        unikatno_ime_vaje = self.unikatno_ime_vaje
        return f"posnetek {ime_posnetka} za {unikatno_ime_vaje}"


    def premakni_vajo(self, v_program):
        self.program = v_program






#UPORABNIK-----------------------------------------------------------------------------------------------------



class Uporabnik:

    def __init__(self, ime, uporabnisko_ime, zasifrirano_geslo, zvezek):
        self.ime = ime
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
    def registracija(ime, uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(ime, uporabnisko_ime, zasifrirano_geslo, Zvezek())
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
            "ime": self.ime,
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "zvezek": self.zvezek.v_slovar()
        }

    @staticmethod
    def iz_slovarja(slovar):
        ime = slovar["ime"]
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        zvezek = Zvezek.iz_slovarja(slovar["zvezek"])
        return Uporabnik(ime, uporabnisko_ime, zasifrirano_geslo, zvezek)




