#!/bin/bash
set -e # zatrzymaj skrypt przy bledzie

cd ../

echo "== Instalacja openbabel z systemu =="
ln -s /usr/lib/python3/dist-packages/openbabel $(find $VIRTUAL_ENV/lib -type d -name "site-packages") || true

echo "== Pobieranie MOPAC =="
wget -nc http://openmopac.net/mopac-23.1.2-linux.tar.gz
tar zxvf mopac-23.1.2-linux.tar.gz

#echo "== Pobieranie JSME =="
#wget -nc https://jsme-editor.github.io/downloads/JSME_2024-04-29.zip
#unzip -o JSME_2024-04-29.zip

echo "== Rozpakowywanie Jmol =="
wget https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.0/Version%2014.0.13/Jmol-14.0.13-binary.tar.gz
tar zxvf Jmol-14.0.13-binary.tar.gz jmol-14.0.13/jsmol.zip
unzip -o jmol-14.0.13/jsmol.zip

echo "== Czyszczenie plików tymczasowych =="
rm -f Jmol-14.0.13-binary.tar.gz

echo "== Przenoszenie jsmol do media =="
mv jsmol programming_project_WCh_2025/mopac_portal/media

#echo "== Przenoszenie jsme do static =="
#mv JSME_2024-04-29/jsme programming_project_WCh_2025/mopac_portal/static

echo "== Instalacja zaleznosci z requirements.txt =="
pip install -r programming_project_WCh_2025/mopac_portal/requirements.txt

echo
echo "============================="
echo "Wszystko gotowe!"
echo "============================="
