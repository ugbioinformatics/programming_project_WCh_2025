from django.views.generic import ListView, DetailView # type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # type: ignore # new
from django.urls import reverse_lazy  # type: ignore # new
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from .forms import Suma
from .forms import Suma2
import subprocess
from .models import Post
import mmap
import pubchempy as pcp  #dodany modul pubchempy dla zastapenia cactus
from .Utilities import make_png_and_mop, heat_energy, metoda
from django.conf import settings




def CIRconvert_Views(request):   #zamienia nam nazwe na smilesa
				 #tworzy wzor molekuly (png)
	#from django.conf import settings
	print('views')
	if request.method == 'POST':
		form = Suma(request.POST)
		if form.is_valid():
			body = form.cleaned_data["pole_nazwa"]

			if body != "":
				# Zamiana nazwy związku na SMILES przez PubChem
				try:
					compound = pcp.get_compounds(body, "name")
					if compound:
						pole_smiles = compound[0].isomeric_smiles
					else:
						pole_smiles = ""
				except Exception as e:
					print("Błąd przy pobieraniu SMILES:", e)
					pole_smiles = ""
			   
				#url = 'http://cactus.nci.nih.gov/chemical/structure/' + body + '/smiles'
				#print('url')
				#pole_smiles = urlopen(url).read().decode('utf8')
				#if request.user.is_authenticated:
				# Uzyskiwanie IUPAC name przez skrypt
				try:
					result = subprocess.run(
						['python3', 'pubchem_convert_SMILES_to_IUPAC.py', pole_smiles],
						capture_output=True,
						text=True
					)
					iupac_name_output = result.stdout.strip()
					print("Wynik skryptu:", iupac_name_output)
				except Exception as e:
					print("Błąd przy uzyskiwaniu IUPAC name:", e)
					iupac_name_output = ""

				if request.user.is_authenticated:
					post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, ionization=0,
								weight=0, grad=0, author=request.user)
				else:
					post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, ionization=0,
								weight=0, grad=0)

				post.iupac_name = iupac_name_output  
				post.save()
				make_png_and_mop(pole_smiles, post.id)

			else:
				pole_smiles = form.cleaned_data["pole_smiles"]
				try:
					compound = pcp.get_compounds(pole_smiles,"smiles")
					if compound and compound[0].iupac_name:
						iupac_name_output = compound[0].iupac_name
						print("IUPAC name:", iupac_name_output)
					else:
						iupac_name_output = "No IUPAC ame found"
				except Exception as e:
					print("Błąd przy pobiernaiu: ",e)
					iupac_name_output = "Error retrieving name"
				if request.user.is_authenticated:
					post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, ionization=0,
								weight=0, grad=0, author=request.user)
				else:
					post = Post(nazwa=body, smiles=pole_smiles, cieplo=0, ionization=0,
								weight=0, grad=0)
				post.iupac_name = iupac_name_output
				post.save()
				make_png_and_mop(pole_smiles,post.id)
			post.metoda = form.cleaned_data["pole_metoda"]
			metoda(post.id, post.metoda)
			subprocess.run(['../mopac.sh', 'molecule.mop'], cwd=settings.MEDIA_ROOT + '/' + str(post.id))
			post.cieplo, post.ionization, post.weight, post.grad = heat_energy(post.id)
			post.save()
			return redirect('/')
	else:
		form = Suma()
	return render(request, 'suma.html', {'form': form})







def CIRconvert_Views_Reaction(request):    #prawd to samo co wyzej tylko, ze do reakcji
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
				post = Post(nazwa=pole_smiles1 + pole_smiles2, smiles1 = pole_smiles1,smiles2 = pole_smiles2, cieplo=0, ionization=0,weight = 0, grad =0, author = request.user)
			else:
				post = Post(nazwa=pole_smiles1 + pole_smiles2, smiles1 = pole_smiles1,smiles2 = pole_smiles2, cieplo=0, ionization=0,weight = 0, grad = 0)
			post.save()
			print(post.id)
			from .Utilities import make_png_and_mop
			make_png_and_mop(pole_smiles1, post.id)	#utilities.py 4
			make_png_and_mop2(pole_smiles2, post.id) 	#utilities.py 16



			post.metoda = form.cleaned_data["pole_metoda"]
			metoda(post.id,post.metoda)
			metoda2(post.id,post.metoda)
			subprocess.run(['../mopac.sh', 'molecule.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
			subprocess.run(['../mopac.sh', 'molecule2.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))
			post.cieplo1, post.energia1 = heat_energy(post.id)
			post.cieplo2, post.energia2 = heat_energy(post.id)
			post.save()

			from django.conf import settings
			with open(settings.MEDIA_ROOT+'/'+str(post.id)+"/saddle.mop", 'w+') as file:
				file.write("geo_dat='molecule.arc' +" + "\n")
				file.write("geo_ref='molecule2.arc' +" + "\n")
				file.write("saddle html xyz  bar=0.005" + "\n")
				file.write("Locating transition state using SADDLE" + "\n")
			subprocess.run(['../mopac.sh', 'saddle.mop'], cwd = settings.MEDIA_ROOT+'/'+str(post.id))



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


			subprocess.run(['../mopac.sh', 'ts.mop'], cwd=settings.MEDIA_ROOT+'/'+str(post.id))
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

def Calculate(request,pk):    		#wyswietla obliczenia
	from .Utilities import calculate  	# utilities.py 54
	post = get_object_or_404(Post, pk=pk)
	calculate(post, pk)
	post.calculated = True
	post.save()
	return render(request, 'post_detail.html', {'post': post})

class BlogListView(ListView):		#szuka ktora funckja powinna byc wyswietlana ktorym html'em w naszym folderze
	model = Post
	template_name = "home.html"
	def get_queryset(self, **kwargs):
		qs = super().get_queryset(**kwargs)
		if self.request.user.is_authenticated:
			return qs.filter(author=self.request.user)
		else:
			return qs.filter(author=None)
		
#odpowiada za wrzucanie wartosci do strony (nie odpowiadamy za to)
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


class BlogDeleteView(DeleteView):  
	model = Post
	template_name = "post_delete.html"
	success_url = reverse_lazy("home")
