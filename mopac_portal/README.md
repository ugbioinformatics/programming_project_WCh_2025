# programming_project_WCh_2024 - MOPAC GUI

<h2>Django web portal do obliczeń w programie MOPAC</h2>

MOPAC produkuje wyniki jako strony html z animacjami z wykorzystaniem Jmol.
          
<i> Instructions to allow Firefox to open local HTML files that use Jmol.

(1) Open Firefox. Go to the URL about:config (type this in the URL bar at the top of the Firefox window.)

(2) Set the switch "security.fileuri.strict_origin_policy" to "false" - this can be done by clicking on the switch.
</i>

<h3>Instalacja virtualnego środowiska python3 z systemowym openbabel</h3>
<pre>
python3 -m venv env
source env/bin/activate.csh
ln -s /usr/lib/python3/dist-packages/openbabel $VIRTUAL_ENV/lib/python*/site-packages
</pre>

<h3> Mopac </h3>
pobieramy ze strony http://openmopac.net/Download_MOPAC_Executable_Step2.html
<pre>
wget https://github.com/openmopac/mopac/releases/download/v23.2.3/mopac-23.2.3-linux.tar.gz
tar zxvf mopac-23.2.3-linux.tar.gz 
</pre>

<h3>Nasza aplikacja django pobierana z github</h3>
<pre>
git clone https://github.com/ugbioinformatics/programming_project_WCh_2025.git
pip install -r programming_project_WCh_2025/mopac_portal/requirements.txt
</pre>

<h3> Jmol </h3>
używany przez strony html generowane przez mopac
<pre>
wget https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.0/Version%2014.0.13/Jmol-14.0.13-binary.tar.gz
tar zxvf Jmol-14.0.13-binary.tar.gz jmol-14.0.13/jsmol.zip
unzip jmol-14.0.13/jsmol.zip    
rm Jmol-14.0.13-binary.tar.gz
mv jsmol programming_project_WCh_2025/mopac_portal/media                    
</pre>

<h3> JSME Molecule Editor </h3>
JSME pozwala na narysowanie czasteczki i wygenerowanie na tej podstawie
SMILES, pobieramy aplikacje JSME i przenosimy do static
<pre>
wget https://jsme-editor.github.io/downloads/JSME_2024-04-29.zip
unzip JSME_2024-04-29.zip
mv JSME_2024-04-29/jsme programming_project_WCh_2025/mopac_portal/static
</pre>

<h3>startujemy aplikację</h3>
<pre>
cd programming_project_WCh_2025/mopac_portal
python3 manage.py makemigrations blog
python3 manage.py migrate
python3 manage.py runserver
</pre>

