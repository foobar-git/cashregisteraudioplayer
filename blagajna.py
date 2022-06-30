# Blagajna v0.99                                         KONZUM d.o.o.
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
string_status = None                # varijabla za statusni string
prekid = False                      # var za prekid reprodukcije zvuka
prekid_ = False                     # radna kopija br_b za rad sa memorijom
otvaranje_blagajne = False          # da li je proces otvaranja u toku
audio_seReproducira = False         # stanje reprodukcije zvuka
niz_status_blagajni = []            # stanje blagajni (otvoreno ili zatvoreno)
aktivna_blagajna = None             # blagajna s kojom manipulišemo u datom trenu
br_blagajne_interfejsFiksno = None  # broj pojedinačne blagajne koji proslijeđuje interfejs
                                    # i koji je fiksan, npr. za blagajnu broj 1, interfejs
                                    # će uvijek proslijediti broj 1. Drugim riječima,
                                    # ovim brojem se identificira blagajna koja šalje
                                    # API upit.
br_druge_blagajne = None            # broj blagajne na koju se odnosi upit, npr. blagajna
                                    # broj 1 otvara blagajnu broj 2.
br_b = []                           # broj blagajne iz upita na osnovu kojeg se formira niz
                                    # za manipulaciju statusima
br_b_ = []                          # radna kopija br_b za rad sa memorijom
broj_jezika = None                  # broj jezika (npr. za četiri jezika je 4)
broj_blagajni = 1                   # unijeti broj blagajni koje se koriste
br_blagajni = None                  # radna kopija br_blagajni za rad sa memorijom
jezici = ["bh", "en"]               # unijeti jezike (npr. dodati "de" za njemački) da bude
                                    # jezici = ["bh", "en", "de"]


# FUNKCIJE =============================================================

# reprodukcija zvučnog zapisa za otvaranje
def fn_odaberiJezik_otvaranje(i):
    jezici_ = jezici
    global broj_jezika              
    broj_jezika = len(jezici)       # na osnovu niza "jezici" formira se broj jezika
    
    for j in range(broj_jezika):
        fname = 'b' + str(i) + '_' + '1' + '_' + jezici[j] + '.sh'
        fname = './scripts/' + fname
        subprocess.run([ 'sh', fname ])

# reprodukcija zvučnog zapisa za zatvaranje        
def fn_odaberiJezik_zatvaranje(i):
    jezici_ = jezici
    global broj_jezika
    broj_jezika = len(jezici)       # na osnovu niza "jezici" formira se broj jezika
    
    for j in range(broj_jezika):
        fname = 'b' + str(i) + '_' + '0' + '_' + jezici[j] + '.sh'
        fname = './scripts/' + fname
        subprocess.run([ 'sh', fname ])

# postavljanje blagajne s kojom se manipuliše u datom trenu
def fn_set_aktivna_blagajna(b, s):
    aktivna_blagajna = br_druge_blagajne
    global prekid_
    prekid_ = prekid
    string_status = "Status: Reprodukcija audio datoteke je u toku."
    
    if prekid_ == False:
        niz_status_blagajni[b - 1] = s;
        print(niz_status_blagajni)
        string_status = "Status: Blagajna " + str(b) + " je otvorena."
        string_status += noviRed + "Status: Reprodukcija audio datoteka je završena."

# označavanje stanja aktivne blagajne u "zatvoreno" (0 = zatvoreno)
def fn_set_neaktivna_blagajna(b):
    print('fn_set_neaktivna_blagajna()')
    niz_status_blagajni[b - 1] = 0;
    print(niz_status_blagajni)

# prekid zatvaranja blagajne (ako se greškom pozove zatvaranje blagajne)
def fn_set_prekid_zatvaranja(b):
    print('fn_set_prekid_zatvaranja()')
    niz_status_blagajni[b - 1] = 1;
    print(niz_status_blagajni)

# pri prvom pokretanju aplikacije, kreira se niz za statuse blagajni (sve zatvorene)
def fn_kreiraj_niz_status_blagajni(b):
    stanje = 2                          # stanje 1 ili 0 (otvoreno ili zatvoreno)
    global niz_status_blagajni
    niz_status_blagajni = []
    niz_status_blagajni = [0] * b       # kreiraj niz na osnovu broja_blagajni
    print(niz_status_blagajni)
    return 'Status: Niz je kreiran (niz_status_blagajni).'

# pregled bitnih varijabli i niza
def fn_debuglog():
    print('aktivna_blagajna: ' + str(aktivna_blagajna))
    print('broj_blagajne_interfejsFiksno: ' + str(br_blagajne_interfejsFiksno))
    print('broj_druge_blagajne: ' + str(br_druge_blagajne))
    print('debug: niz_status_blagajni: ' + str(niz_status_blagajni))

# testna funkcija, za testiranje
def fn_test():
    print('debug: niz_status_blagajni: ' + str(niz_status_blagajni))


# FLASK ================================================================

from flask import Flask, current_app
app = Flask(__name__)


# API ==================================================================

@app.route("/")
def index():
    return current_app.send_static_file('index.html')

@app.route("/0/1/<int:broj_blagajne_interfejsFiksno>/<int:broj_druge_blagajne>")
# otvaranje blagajne
def fn_otvori_blagajnu(broj_blagajne_interfejsFiksno, broj_druge_blagajne):
    global prekid
    prekid = False
    
    global otvaranje_blagajne
    otvaranje_blagajne = True
    
    global audio_seReproducira
    global aktivna_blagajna
    
    global br_blagajne_interfejsFiksno
    br_blagajne_interfejsFiksno = broj_blagajne_interfejsFiksno
    global br_druge_blagajne
    br_druge_blagajne = broj_druge_blagajne
    
    global br_b
    print('br_b: ' + str(br_b))
    br_b.append(broj_druge_blagajne)
    print('br_b: ' + str(br_b))
    
    aktivna_blagajna = broj_blagajne_interfejsFiksno

    # logika za sprečavanje ispreplitanja zvuka
    if aktivna_blagajna == broj_druge_blagajne:
        if audio_seReproducira == False:
            audio_seReproducira = True
            fn_odaberiJezik_otvaranje(br_blagajne_interfejsFiksno)
            audio_seReproducira = False
    else:
        if audio_seReproducira == False:
            audio_seReproducira = True
            fn_odaberiJezik_otvaranje(br_druge_blagajne)
            audio_seReproducira = False
    
    if audio_seReproducira == False:
        br_b.append(broj_druge_blagajne)
        print('br_b: ' + str(br_b))
    else:
        br_b.pop()
        print('br_b: ' + str(br_b))
    
    global br_b_
    br_b_ = []                      # kopiramo u novi niz zadnja dva elementa
    if len(br_b) > 1:
        br_b_.append(br_b[-2])      # predzadnji
    if len(br_b) < 2:
        br_b_.append(br_b[-1])      # zadnji
    
    if len(br_b) > 3:               # ovo osigurava da je maksimalan broj
        br_b.pop(1)                 # elemenata u nizu 4 (testirano)
    print("br_b_" + str(br_b_))
    
    fn_set_aktivna_blagajna(br_b_[-1], 1) #uzmi zadnji element iz niza
    string_status = 'Status: Blagajna ' + str(br_druge_blagajne) + ' je otvorena.'
    otvaranje_blagajne = False
    
    return string_status

@app.route("/1/0/<int:broj_blagajne_interfejsFiksno>/<int:broj_druge_blagajne>")
# zatvaranje blagajne
def fn_zatvori_blagajnu(broj_blagajne_interfejsFiksno, broj_druge_blagajne):
    fn_debuglog()
    br_blagajne_interfejsFiksno = broj_blagajne_interfejsFiksno
    br_druge_blagajne = broj_druge_blagajne
    
    # logika za sprečavanje ispreplitanja zvuka
    global audio_seReproducira
    if audio_seReproducira == False:
        audio_seReproducira = True
        
        if br_blagajne_interfejsFiksno == br_druge_blagajne:
            fn_odaberiJezik_zatvaranje(br_blagajne_interfejsFiksno)
            fn_set_aktivna_blagajna(br_druge_blagajne, 0) # 0 = zatvaranje
            string_status = 'Status: Blagajna ' + str(br_druge_blagajne) + ' je zatvorena.'
            
            if prekid == True:
                string_status = 'Status: Zatvaranje je prekinuto.'
                fn_set_prekid_zatvaranja(br_druge_blagajne)
                global prekid
                prekid = False
                
            string_status = 'Status: Zatvaranje je u toku.'
        
        else:
            string_status = 'Status: Aktivna blagajna i broj blagajne se ne podudaraju.'
        
        audio_seReproducira = False
        
    else:
        string_status = "Status: Reprodukcija audio datoteke je u toku (zatvaranje)."
    
    return string_status

@app.route("/9/<int:broj_blagajne_interfejsFiksno>/<int:broj_druge_blagajne>")
# prekid trenutno reproduciranog zvučnog zapisa
def fn_prekid_audio(broj_blagajne_interfejsFiksno, broj_druge_blagajne):
    fn_debuglog()
    
    global prekid
    prekid = True
    
    br_druge_blagajne = broj_druge_blagajne
    br_blagajne_interfejsFiksno = broj_blagajne_interfejsFiksno
    if aktivna_blagajna == br_blagajne_interfejsFiksno:
        # prekid reprodukcije zvuka
        for kp in range(broj_jezika):
            os.system('pkill omxplayer')
            
        if otvaranje_blagajne == True:
            fn_set_neaktivna_blagajna(br_druge_blagajne)
            string_status = 'Status: Otvaranje blagajne' + str(broj_blagajne_interfejsFiksno) + ' je anulirano.'
        else:
            string_status = 'Status: Zatvaranje blagajne' + str(broj_blagajne_interfejsFiksno) + ' je anulirano.'
    
    else:
        string_status = 'Status: Aktivna blagajna i broj blagajne se ne podudaraju.'
    
    return string_status

@app.route("/8/<int:broj_blagajni>")
# prvo pokretanje i kreiranje niza (niz_status_blagajni)
def kreiraj_niz(broj_blagajni):
    global jezici
    
    global br_blagajni
    br_blagajni = broj_blagajni
    
    global string_status
    string_status = ""
    
    global prekid
    prekid = False
    
    print('niz_status_blagajni' + str(niz_status_blagajni))
    return fn_kreiraj_niz_status_blagajni(br_blagajni)
    
@app.route("/test")
# za testiranje
def test():
    fn_test()
    return "<p>This is a test.</p>"

# python main
if __name__ == "__main__":
    app.run()
