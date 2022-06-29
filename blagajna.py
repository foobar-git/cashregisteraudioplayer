# Blagajna v0.9                                         KONZUM d.o.o.
#
# Glavna logika za aplikaciju Blagajna
# za unos novih jezika, u funkcijama "fn_odaberiJezik_otvaranje" i
# "fn_odaberiJezik_zatvaranje", u nizu "jezici[]" dodati novi jezik npr.
# jezici = ["bh", "en", "tr", "de"] itd. Voditi računa o broju
# navedenih jezika, jer će svi navedeni jezici biti # sekvencijalno
# reprodukovani. Ako želite reprodukciju samo jednog # jezika, onda
# navesti samo taj željeni jezik npr. jezici = ["bh"].
#
# API rute se nalaze na dnu datoteke.
#
# Datoteke i folderi neophodni za rad ove aplikacije su:
#   *   "blagajna.py"               -ova datoteka
#   *   ".mkscripts-aux.sh"         -generisanje skripti za 3.5mm aux
#   *   ".mkscripts-hdmi.sh"        -generisanje skripti za hdmi
#   *   "startservers.sh"           -pokretanje flask servera
#   *   "__pycache__"               -cache
#   *   "venv"                      -virtualno okruzenje za flask
#   *   "audio"                     -zvučni snimci
#   *   "scripts"                   -skripte za pokretanje snimaka
#
# ======================================================================

import subprocess
import os
from array import *

# DEFINICIJE ===========================================================

noviRed = "<br>"
prekid = None                   # variabla za prekid reprodukcije zvuka
m_prekid = False                # variabla za prekid reprodukcije zvuka
audio_SeReproducira = False
niz_blagajne = []
aktivna_blagajna = None
br_trenutne_blagajne = None
br_nove_blagajne = None
br_b = []
br_b_ = []
broj_jezika = None


# FUNKCIJE =============================================================

# reprodukcija zvučnog zapisa za otvaranje
def fn_odaberiJezik_otvaranje(i):
    jezici = ["bh", "en"]
    global broj_jezika
    broj_jezika = len(jezici)
    for j in range(broj_jezika):
        fname = 'b' + str(i) + '_' + '1' + '_' + jezici[j] + '.sh'
        fname = './scripts/' + fname
        subprocess.run([ 'sh', fname ])

# reprodukcija zvučnog zapisa za zatvaranje        
def fn_odaberiJezik_zatvaranje(i):
    jezici = ["bh", "en"]
    global broj_jezika
    broj_jezika = len(jezici)
    for j in range(broj_jezika):
        fname = 'b' + str(i) + '_' + '0' + '_' + jezici[j] + '.sh'
        fname = './scripts/' + fname
        subprocess.run([ 'sh', fname ])

def fn_set_aktivna_blagajna(b, s):
    aktivna_blagajna = br_nove_blagajne
    global m_prekid
    global prekid
    m_prekid = prekid
    n_string = "Status: Reprodukcija audio datoteke je u toku."
    if m_prekid == False:
        niz_blagajne[b - 1] = s;
        print(niz_blagajne)
        n_string = "Status: Blagajna " + str(b) + " je otvorena."
        n_string += noviRed + "Status: Reprodukcija audio datoteka je završena."

def fn_set_neaktivna_blagajna(b):
    niz_blagajne[b - 1] = 0;
    print(niz_blagajne)

def fn_set_niz_blagajne():
    broj_blagajnih = 10 # EDIT ovo napraviti dinamično
    stanje = 2          # EDIT i ovo
    global niz_blagajne
    niz_blagajne = []
    """for i in range(broj_blagajnih):
        s = 0
        niz_blagajne.append(s)
        print(niz_blagajne)"""
    niz_blagajne = [0] * broj_blagajnih
    print(niz_blagajne)
    return 'Status: Niz je kreiran.'
    
def fn_debuglog():
    print('aktivna_blagajna: ' + str(aktivna_blagajna))
    print('broj_trenutne_blagajne: ' + str(br_trenutne_blagajne))
    print('broj_nove_blagajne: ' + str(br_nove_blagajne))


# FLASK ================================================================

from flask import Flask, current_app
app = Flask(__name__)


# API ==================================================================

@app.route("/")
def index():
    return current_app.send_static_file('index.html')

@app.route("/0/1/<int:broj_trenutne_blagajne>/<int:broj_nove_blagajne>")
# otvaranje blagajne
def fn_otvori_blagajnu(broj_trenutne_blagajne, broj_nove_blagajne):
    global audio_SeReproducira
    global aktivna_blagajna
    global br_trenutne_blagajne
    br_trenutne_blagajne = broj_trenutne_blagajne
    global br_nove_blagajne
    br_nove_blagajne = broj_nove_blagajne
    
    print('br_b: ' + str(br_b))
    br_b.append(broj_nove_blagajne)
    print('br_b: ' + str(br_b))
    
    aktivna_blagajna = broj_trenutne_blagajne

    # logika za sprečavanje ispreplitanja zvuka
    if aktivna_blagajna == broj_nove_blagajne:
        if audio_SeReproducira == False:
            audio_SeReproducira = True
            fn_odaberiJezik_otvaranje(br_trenutne_blagajne)
            audio_SeReproducira = False
    else:
        if audio_SeReproducira == False:
            audio_SeReproducira = True
            fn_odaberiJezik_otvaranje(br_nove_blagajne)
            audio_SeReproducira = False
    
    if audio_SeReproducira == False:
        br_b.append(broj_nove_blagajne)
        print('br_b: ' + str(br_b))
    else:
        br_b.pop()
        print('br_b: ' + str(br_b))
    
    global br_b
    global br_b_
    br_b_ = []                  # kopiramo u novi niz zadnja dva elementa
    br_b_.append(br_b[-2])      # zadnji
    br_b_.append(br_b[-1])      # predzadnji
    br_b = br_b_.copy()         # "očisti" niz
    print("br_b_" + str(br_b_))
    fn_set_aktivna_blagajna(br_b_[-1], 1) #uzmi zadnji element iz niza
    return 'mama ti je return' # EDIT srediti

@app.route("/1/0/<int:broj_trenutne_blagajne>/<int:broj_nove_blagajne>")
# zatvaranje blagajne
def fn_zatvori_blagajnu(broj_trenutne_blagajne, broj_nove_blagajne):
    fn_debuglog()
    br_trenutne_blagajne = broj_trenutne_blagajne
    br_nove_blagajne = broj_nove_blagajne
    
    # logika za sprečavanje ispreplitanja zvuka
    global audio_SeReproducira
    if audio_SeReproducira == False:
        audio_SeReproducira = True
        if br_trenutne_blagajne == br_nove_blagajne:
            fn_odaberiJezik_zatvaranje(br_trenutne_blagajne)
            fn_set_aktivna_blagajna(br_nove_blagajne, 0)
            #print(niz_blagajne)
            n_string = 'Status: Blagajna ' + str(br_nove_blagajne) + ' je zatvorena.'
        else:
            n_string = 'Status: Aktivna blagajna i broj blagajne se ne podudaraju.'
        
        audio_SeReproducira = False
        
    else:
        n_string = "Status: reprodukcija je u toku (zatvaranje)."
    
    return n_string

@app.route("/9/<int:broj_trenutne_blagajne>/<int:broj_nove_blagajne>")
# prekid trenutno reproduciranog zvučnog zapisa
def fn_prekid_audio(broj_trenutne_blagajne, broj_nove_blagajne):
    fn_debuglog()
    prekid = True
    br_nove_blagajne = broj_nove_blagajne
    br_trenutne_blagajne = broj_trenutne_blagajne
    if aktivna_blagajna == br_trenutne_blagajne:
        for kp in range(broj_jezika):
            os.system('pkill omxplayer')
        #return 'Status: PREKID reprodukcije zvuka.'
        fn_set_neaktivna_blagajna(br_nove_blagajne)
        n_string = 'Status: broj trenutne blagajne (fiksno) je anuliran.'
    else:
        n_string = 'Status: Aktivna blagajna i broj blagajne se ne podudaraju.'
    
    return n_string

@app.route("/8")
# prvo pokretanje i kreiranje niza (niz_blagajne)
def kreiraj_niz():
    #global br_b
    global prekid
    prekid = False
    print('niz_blagajne' + str(niz_blagajne))
    return fn_set_niz_blagajne()
    
@app.route("/test")
# za testiranje
def test():
    #fn_test()
    return "<p>This is a test.</p>"

# python main
if __name__ == "__main__":
    app.run()
