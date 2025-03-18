def make_png_and_mop(smiles, id):
    import openbabel.pybel
    import os
    from django.conf import settings
    czasteczka = openbabel.pybel.readstring("smi", smiles)
    os.mkdir(settings.MEDIA_ROOT+'/'+str(id))
    czasteczka.write(format="svg",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.svg", overwrite=True)
    czasteczka.make3D()
    czasteczka.write(format="mop",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mop",overwrite=True)
    czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/start.mol2",overwrite=True)

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




def smile_check(smiles):
    import openbabel.pybel
    import os
    try:
        czasteczka = openbabel.pybel.readstring("smi", smiles)
        return 'it work'
    except:
        return 'it dont work'

def CIRconvert(ids):
    from urllib.request import urlopen
    from urllib.parse import quote
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(ids) + '/smiles' 
        print(url)
        return urlopen(url).read().decode('utf8')
    except:
        return 'Did not work'


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
    

