from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # new
from django.urls import reverse_lazy  # new
from django.shortcuts import get_object_or_404, render, redirect
from .forms import Suma
from .forms import Suma2
import subprocess
from .models import Post
import mmap
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
def metoda(id,metoda):
    import fileinput
    from django.conf import settings
    
    with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mop", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('PUT KEYWORDS HERE',metoda + " html"), end='')
    return
    

def metoda2(id,metoda):
    import fileinput
    from django.conf import settings
    
    with fileinput.FileInput(settings.MEDIA_ROOT+'/'+str(id)+"/molecule2.mop", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('PUT KEYWORDS HERE',metoda + " html"), end='')
    return


def heat_energy(id):
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
        if line.startswith('          TOTAL ENERGY            ='):
            energy = float(line.split()[-2])
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
    plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/nalesnik.png")
    plt.close()
    plt.plot(HEAT)
    plt.savefig(settings.MEDIA_ROOT+'/'+str(id)+"/placek.png")
    plt.close()
    czasteczka = next(openbabel.pybel.readfile("mopout", settings.MEDIA_ROOT+'/'+str(id)+"/molecule.out"))
    
    
    czasteczka.write(format="mol2",filename=settings.MEDIA_ROOT+'/'+str(id)+"/molecule.mol2",overwrite=True)
    
    return heat, energy

def heat_energy2(id):
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
        if line.startswith('          TOTAL ENERGY            ='):
            energy = float(line.split()[-2])
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
    
    return heat, energy

def CIRconvert_Views(request):
    from django.conf import settings
    print('views')
    if request.method == 'POST':
        form = Suma(request.POST)
        if form.is_valid():
            from urllib.request import urlopen
            from urllib.parse import quote
            print('if is valid')
            body = form.cleaned_data["pole_nazwa"]
            if body != "":        
                url = 'http://cactus.nci.nih.gov/chemical/structure/' + body + '/smiles'
                print('url')
                pole_smiles = urlopen(url).read().decode('utf8')
                if request.user.is_authenticated:
                    post = Post(nazwa=body, smiles=pole_smiles,cieplo=0, energia=0, author = request.user)
                else:
                    post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, energia=0)
                post.save()
                print(post.id)
                from .Utilities import make_png_and_mop
                make_png_and_mop(pole_smiles, post.id)
                
            else:
                pole_smiles = form.cleaned_data["pole_smiles"]
                if request.user.is_authenticated:
                    post = Post(nazwa=pole_smiles, smiles = pole_smiles,cieplo=0, energia=0, author = request.user)
                else:
                    post = Post(nazwa=pole_smiles, smiles = pole_smiles,cieplo=0, energia=0)
                post.save()
                print(post.id)
                from .Utilities import make_png_and_mop
                make_png_and_mop(pole_smiles, post.id)
            post.metoda = form.cleaned_data["pole_metoda"]
            metoda(post.id,post.metoda)
            subprocess.run(['/opt/mopac/MOPAC2016.exe', 'molecule.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
            post.cieplo, post.energia = heat_energy(post.id)
            post.save()
            return redirect('/')
    else:
        form = Suma()
    return render(request, 'suma.html', {'form': form })






def CIRconvert_Views_Reaction(request):
    from django.conf import settings
    print('views')
    if request.method == 'POST':
        form = Suma2(request.POST)
        if form.is_valid():
            from urllib.request import urlopen
            from urllib.parse import quote
 #           print('if is valid')
#            body = form.cleaned_data["pole_nazwa"]
#            if body != "":        
#                url = 'http://cactus.nci.nih.gov/chemical/structure/' + body + '/smiles'
#                print('url')
#                pole_smiles = urlopen(url).read().decode('utf8')
#                if request.user.is_authenticated:
#                    post = Post(nazwa=body, smiles=pole_smiles,cieplo=0, energia=0, author = request.user)
#                else:
#                    post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, energia=0)
#                post.save()
#                print(post.id)
#                from .Utilities import make_png_and_mop
#                make_png_and_mop(pole_smiles, post.id)
                
#            else:
#                pole_smiles = form.cleaned_data["pole_smiles"]
#                if request.user.is_authenticated:
#                    post = Post(nazwa=pole_smiles, smiles = pole_smiles,cieplo=0, energia=0, author = request.user)
#                else:
#                    post = Post(nazwa=pole_smiles, smiles = pole_smiles,cieplo=0, energia=0)
#                post.save()
#                print(post.id)
#                from .Utilities import make_png_and_mop
#                make_png_and_mop(pole_smiles, post.id)
            from .Utilities import make_png_and_mop, make_png_and_mop2 
            pole_smiles1 = form.cleaned_data["pole_smiles1"]
            pole_smiles2 = form.cleaned_data["pole_smiles2"]
            if request.user.is_authenticated:
                post = Post(nazwa=pole_smiles1 + pole_smiles2, smiles1 = pole_smiles1,smiles2 = pole_smiles2, cieplo=0, energia=0, author = request.user)
            else:
                post = Post(nazwa=pole_smiles1 + pole_smiles2, smiles1 = pole_smiles1,smiles2 = pole_smiles2, cieplo=0, energia=0)
            post.save()
            print(post.id)
            from .Utilities import make_png_and_mop
            make_png_and_mop(pole_smiles1, post.id)
            make_png_and_mop2(pole_smiles2, post.id)



            post.metoda = form.cleaned_data["pole_metoda"]
            metoda(post.id,post.metoda)
            metoda2(post.id,post.metoda)
            subprocess.run(['/opt/mopac/MOPAC2016.exe', 'molecule.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
            subprocess.run(['/opt/mopac/MOPAC2016.exe', 'molecule2.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
            post.cieplo1, post.energia1 = heat_energy(post.id)
            post.cieplo2, post.energia2 = heat_energy(post.id)
            post.save()

            from django.conf import settings
            with open(settings.MEDIA_ROOT+'/'+str(post.id)+"/saddle.mop", 'w+') as file:
                file.write("geo_dat='molecule.arc' +" + "\n")
                file.write("geo_ref='molecule2.arc' +" + "\n")
                file.write("saddle html xyz  bar=0.005" + "\n")
                file.write("Locating transition state using SADDLE" + "\n")
            subprocess.run(['/opt/mopac/MOPAC2016.exe', 'saddle.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))



            with open(settings.MEDIA_ROOT+'/'+str(post.id)+"/saddle.out") as file:
                print("file open")
                for line in file:
                    if "Empirical Formula" in line:
                        aaa = int(line.split()[-2])
                        print(aaa)
                        print(aaa)
                        print(aaa)
                        print(aaa)
                        print(aaa)

#                    print(line)

            with open(settings.MEDIA_ROOT+'/'+str(post.id)+"/saddle.out", 'r') as f:   
 
                m = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)                          
                i = m.rfind(b'Locating transition state using SADDLE')   
                m.seek(i)             
                line = m.readline()   
                line=m.readline()
                nextline=[]
                for ii in range(aaa):
                    line=m.readline()
                    nextline.append(line.decode("utf-8"))
                    
                print (nextline)
            with open(settings.MEDIA_ROOT+'/'+str(post.id)+"/ts.mop", 'w+') as file:
                 file.write("TS html " + "\n")
                 file.write(" " + "\n" )
                 file.write(" " + "\n")
                 for iii in nextline:
                     file.write( iii )
                 file.write("  " + "\n")
                 file.write("oldgeo html irc=1*")


            subprocess.run(['/opt/mopac/MOPAC2016.exe', 'ts.mop'], cwd=settings.MEDIA_ROOT+'/'+str(post.id))
            return redirect('/')
    else:
        form = Suma2()
    return render(request, 'suma.html', {'form': form })
"""
def suma(request):
      if request.method == 'POST':
          form = Suma(request.POST)
          if form.is_valid():
              body = form.cleaned_data["body"]
              title ='SMILES'
              author = "test"
              tmp=body.split()
              for i in range(0, len(tmp)):
                    tmp[i]=int(tmp[i])  
              suma=sum(tmp)
              post = Post(body=body, title=title, author=author,suma=suma)
                       
              post.save()
              return redirect('/')
      else:
          form = Suma()
      return render(request, 'suma.html', {'form': form })
"""

def Calculate(request,pk):
    from .Utilities import calculate
    post = get_object_or_404(Post, pk=pk)
    calculate(post, pk)
    post.calculated = True
    post.save()
    return render(request, 'post_detail.html', {'post': post})

class BlogListView(ListView):
    model = Post
    template_name = "home.html"
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            return qs.filter(author=self.request.user)
        else:
            return qs.filter(author=None)
        
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body", "liczby","suma"]


class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body", "liczby"]


class BlogDeleteView(DeleteView):  # new
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
