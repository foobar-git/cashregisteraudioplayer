#!/bin/bash

# Generisanje skripti za AUX (audio jack 3.5mm) izlaz
#
# Unijeti broj blagajni N (svaka blagajna treba da ima po jednu audio
# datoteku za stanje "otvoreno" i "zatvoreno", te iste datoteke sa
# prevodom na strani jezik)

# Broj blagajnih
N=10

# Priprema za izračunavanje potrebnih skripti
range={1..$N}
range=$(eval echo $range)

# Glavna logika
for i in $range; do
	languages=('bh' 'en') # prostor za dodavanje novih jezika
	for lang in "${languages[@]}"; do
		echo "omxplayer -o local ./audio/b"$i"_o_$lang.mp3" > "./scripts/b"$i"_o_$lang.sh"
		echo "omxplayer -o local ./audio/b"$i"_z_$lang.mp3" > "./scripts/b"$i"_z_$lang.sh"
	done
done
