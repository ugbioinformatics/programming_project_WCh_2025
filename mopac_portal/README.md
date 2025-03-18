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

<h3>Nasza aplikacja django z Jmol</h3>
<pre>
wget https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.0/Version%2014.0.13/Jmol-14.0.13-binary.tar.gz
tar zxvf Jmol-14.0.13-binary.tar.gz
unzip jmol-14.0.13/jsmol.zip          
git clone git@github.com:ugbioinformatics/programming_project_WCh_2024.git
cd programming_project_WCh_2024          
pip install -r requirements.txt
cd abecadlo/
mv ../../jsmol media
python3 manage.py makemigrations blog
python3 manage.py migrate
python3 manage.py runserver
</pre>


