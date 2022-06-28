# Blagajna v0.9                                         KONZUM d.o.o.
#
# Glavna logika za aplikaciju Blagajna
# za unos novih jezika, u funkciji "fn_languages", u nizu "languages[]"
# dodati novi jezik npr. languages = ["bh", "en", "tr", "de"] itd.
# API rute se nalaze na dnu datoteke.
# Datoteke i folderi neophodne za rad ove aplikacije su:
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

# DEFINICIJE ===========================================================

audioPlaying = False


# FUNKCIJE =============================================================

def fn_language(i, s):
    languages = ["bh", "en"]
    for lang in range(len(languages)):
        fname = 'b' + str(i) + '_' + s + '_' + languages[lang] + '.sh'
        fname = './scripts/' + fname
        subprocess.run([ 'sh', fname ])


# FLASK ================================================================
from flask import Flask, current_app
app = Flask(__name__)


# API ==================================================================
@app.route("/")
def index():
    return current_app.send_static_file('index.html')

@app.route("/blagajna/<int:audio_i>/<status>")
def fn_blagajna(audio_i, status):
    global audioPlaying
    if audioPlaying == False:
        audioPlaying = True
        fn_language(audio_i, status)
        audioPlaying = False
    return 'Status: audio datoteke učitane.'

@app.route("/blagajna/prekid")
def prekid():
    os.system('pkill omxplayer')
    return 'PREKID'

@app.route("/test")
def test():
    return "<p>This is a test.</p>"


if __name__ == "__main__":
    app.run()
