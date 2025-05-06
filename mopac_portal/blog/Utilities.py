#funkcje obliczeniowe

# tworzenie wzoru i struktury 3D
def make_png_and_mop(smiles, id):
    import openbabel.pybel
    import os
    from django.conf import settings
    czasteczka = openbabel.pybel.readstring("smi", smiles)
    os.makedirs(settings.MEDIA_ROOT + '/' + str(id), exist_ok=True)
    czasteczka.write(format="svg",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.svg", overwrite=True)
    czasteczka.make3D()
    czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mop",overwrite=True)
    czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/start.mol2",overwrite=True)
    
# tworzenie wzoru i struktury 3D
def make_png_and_mop2(smiles, id):
    import openbabel.pybel
    import os
    from django.conf import settings
    czasteczka = openbabel.pybel.readstring("smi", smiles)
#    os.mkdir(settings.MEDIA_ROOT+'/'+str(id))
    czasteczka.write(format="_png2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.png", overwrite=True)
    czasteczka.make3D()
    czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.mop",overwrite=True)
    czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/start2.mol2",overwrite=True)



#sprawdza poprawnosc smilesa

def smile_check(smiles):
    import openbabel.pybel
    try:
        czasteczka = openbabel.pybel.readstring("smi", smiles)
        return 'it work'
    except Exception as e:
        return 'it dont work'


def CIRconvert(name):
    """
    Konwertuje nazwę związku chemicznego na ciąg SMILES, używając PubChem.
    """
    try:
        compounds = pcp.get_compounds(name, 'name')
        if compounds:
            return compounds[0].isomeric_smiles
        else:
            return 'No compound found'
    except Exception as e:
        return f'Error: {e}'


#oblicza ta duza tablice wartosci

def calculate(post, id):
    import openbabel.pybel
    from django.conf import settings
    import fileinput
    import subprocess
    import re


    czasteczka = next(openbabel.pybel.readfile("mopout",settings.MEDIA_ROOT+'/'+str(id)+"/molecule.out"))
    czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+"/force.mop",overwrite=True)
#    czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+"/drc.mop",overwrite=True)
    metoda = post.metoda
    with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+"/force.mop", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('PUT KEYWORDS HERE',f"{metoda} force"), end='')
    subprocess.run(['../mopac.sh', 'force.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
    



    with open(settings.MEDIA_ROOT+'/'+str(id)+"/force.out", 'r') as file:
        nazwa = file.readlines()
#        post.calculations = nazwa
        post.save()

        out = ""
        index = 0
        out_count = 0
        for line in nazwa:
#            if line == "          DESCRIPTION OF VIBRATIONS\n":
#                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            if "VIBRATION" in line:
                if line == "          DESCRIPTION OF VIBRATIONS\n":
#                    print("CCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDddd")
                    continue
#                print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
                out_temp = line
                out_temp = out_temp.replace(" VIBRATION", f'<a href="/media/{post.id}/drc{out_count+1}.html"> VIBRATION </a>')
                out = out + out_temp
                for i in range(2,8):
                    out = out + nazwa[index + i]
                    
#                print(out)
                out_count = out_count + 1

#            if line == "           FORCE CONSTANT IN CARTESIAN COORDINATES (Millidynes/A)\n":
#                print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
#            print(line)
            index = index + 1
#        print(out_count)
#        post.calculations = out
#            post.vibration_count = (out_count)
#                out = out.replace(" VIBRATION", f'<a href="/media/{post.id}/drc{out_count}.html"> VIBRATION </a>')
#                out = re.sub()
        post.calculations = out
#        print(re.findall("href", out), len(re.findall("href", out)), out_count)
        post.vibration_count = (out_count)
        post.save()
#        print(out)
        #print(out)
        #print("kalkulator chemiczny")

    for i in range(1,post.vibration_count+1):
        czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+f"/drc{i}.mop",overwrite=True)
    
    
        with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+f"/drc{i}.mop", inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace('PUT KEYWORDS HERE',f"{metoda} irc={i}* DRC BIGCYCLES=1 html t-priority=0.5"), end='')

        subprocess.run(['../mopac.sh', f'drc{i}.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
    post.calculated = True
    post.save()
    
def metoda(id,metoda):          #wyrzuca angstromy dla at. w zwiazku
				#z pliku molecule.mop
	import fileinput
	from django.conf import settings
	
	with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mop", inplace=True, backup='.bak') as file:
		for line in file:
			print(line.replace('PUT KEYWORDS HERE',metoda + " html"), end='')
	return
	

def metoda2(id,metoda):		#to samo co metoda, tylko dla drugiej 
				#molekuły
	import fileinput
	from django.conf import settings
	
	with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.mop", inplace=True, backup='.bak') as file:
		for line in file:
			print(line.replace('PUT KEYWORDS HERE',metoda + " html"), end='')
	return


def heat_energy(id):		#funckja wyświetlania wartości
				#z pliku molecule.out
	from django.conf import settings
	import openbabel.pybel
	import os
	import matplotlib.pyplot as plt
	
	with open(settings.MEDIA_ROOT+'/'+str(id)+"/molecule.out", 'r') as file:
		nazwa = file.readlines()
	
	GRAD = []
	HEAT = []
	ionization = 0
	weight = 0
	grad = 0
	for line in nazwa: 		#tu wyświetla wartości liczbowe wybranych właściwości						
		if line.startswith('          FINAL HEAT OF FORMATION ='):
			heat = float(line.split()[-2])
		if line.startswith('          IONIZATION POTENTIAL    ='):
			ionization = float(line.split()[-2])
		if line.startswith('          MOLECULAR WEIGHT        ='):
			weight = float(line.split()[-4])
		if line.startswith('		GRADIENT	      ='):
			grad = float(line.split()[-5])
		if line.startswith(' CYCLE:'):
			a = line.split(":")
#            GRAD.append(float(c.split()[-2]))
			c = a[-2]
#            c.split()[-2]
			HEAT.append(float(a[-1]))
			GRAD.append(float(c.split()[-2]))
			print(line)
#    print(GRAD)
#    print(HEAT)
	plt.plot(GRAD)			#tworzy grafy dla gradie
	plt.xlabel('Cycle')
	plt.ylabel('Gradient')
	plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/nalesnik.png")
	plt.close()
	plt.plot(HEAT)
	plt.xlabel('Cycle')
	plt.ylabel('Heat [Kcal/mol]')
	plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/placek.png")
	plt.close()
	czasteczka = next(openbabel.pybel.readfile("mopout", settings.MEDIA_ROOT+'/'+str(id)+"/molecule.out"))
	
	czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mol2",overwrite=True) #pewnie cos do wizualizacji
	
	return heat, ionization, weight, grad
	
#funkcje są podwojone, ponieważ są potrzebne dla osobnych molekuł
#zeby potem zaimplementowac do reakcji
"""
def suma_old(request,pk):
	post = get_object_or_404(Post, pk=pk)
	tmp=post.liczby.split()
	for i in range(0, len(tmp)):
		tmp[i]=int(tmp[i])  
	post.suma=sum(tmp)
	post.save()
	return render(request, 'post_detail.html', {'post': post})
"""

'''
def heat_energy2(id):		#funckja wyświetlania wartości
				#z pliku molecule.out
				#jest niekompletna - wrocic
	from django.conf import settings
	import openbabel.pybel
	import os
	import matplotlib.pyplot as plt
	
	with open(settings.MEDIA_ROOT+'/'+str(id)+"/molecule.out", 'r') as file:
		nazwa = file.readlines()
	
	GRAD = []
	HEAT = []
	for line in nazwa:
		if line.startswith('          FINAL HEAT OF FORMATION ='):
			heat = float(line.split()[-2])
		if line.startswith('          IONIZATION POTENTIAL    ='):
			ionization = float(line.split()[-2])
		if line.startswith('          MOLECULAR WEIGHT        ='):
			weight = float(line.split()[-2])
		if line.startswith(' CYCLE:'):
			a = line.split(":")
#            GRAD.append(float(c.split()[-2]))
			c = a[-2]
#            c.split()[-2]
			HEAT.append(float(a[-1]))
			GRAD.append(float(c.split()[-2]))
#    print(GRAD)
#    print(HEAT)
	plt.plot(GRAD)
	plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/nalesnik2.png")
	plt.close()
	plt.plot(HEAT)
	plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/placek2.png")
	plt.close()
	czasteczka = next(openbabel.pybel.readfile("mopout", settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.out"))
   
	
	czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.mol2",overwrite=True)
	
	return heat, ionization, weight, grad
'''
	

