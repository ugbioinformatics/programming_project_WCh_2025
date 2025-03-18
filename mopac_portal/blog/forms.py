from django import forms
from .models import Post
import datetime
from .Utilities import CIRconvert, smile_check


class Suma(forms.Form):
    pole_nazwa = forms.CharField(label='Name', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
    pole_smiles = forms.CharField(label='SMILES', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
    #data1 = forms.DateField(initial=datetime.date.today,label="Podaj datę",help_text="data obliczeń")
    #URL = forms.URLField()
    #bool = forms.BooleanField()
    pole_metoda = forms.ChoiceField(choices = (("AM1", "AM1"), ("PM7", "PM7"), ("PM3", "PM3"), ("RM1", "RM1"), ))
    
    def clean(self):
        cleaned_data = super(Suma, self).clean()
        pole_nazwa = cleaned_data.get("pole_nazwa")
        pole_smiles = cleaned_data.get("pole_smiles")
        
        if pole_nazwa == "" and pole_smiles == "":  #brak nazwy i smiles
            self.add_error('pole_nazwa','podaj dane')
        
        if pole_nazwa != "" and pole_smiles == "":  #brak smiles
            if CIRconvert(pole_nazwa)=='Did not work':
                self.add_error('pole_nazwa','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa == "" and pole_smiles != "":  #brak nazwy
            if smile_check(pole_smiles)=='it dont work':
                self.add_error('pole_smiles','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa != "" and pole_smiles != "":  #podana nazwa i smiles
            self.add_error('pole_nazwa','wszystkie pola wypełnione')

class Suma2(forms.Form):
#    pole_nazwa = forms.CharField(label='Name', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
    pole_smiles1 = forms.CharField(label='SMILES1', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
#    pole_nazwa2 = forms.CharField(label='Name', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
    pole_smiles2 = forms.CharField(label='SMILES2', required = False,widget=forms.TextInput(attrs={'size':40, 'maxlength':400}))
    #data1 = forms.DateField(initial=datetime.date.today,label="Podaj datę",help_text="data obliczeń")
    #URL = forms.URLField()
    #bool = forms.BooleanField()
    pole_metoda = forms.ChoiceField(choices = (("AM1", "AM1"), ("PM7", "PM7"), ("PM3", "PM3"), ("RM1", "RM1"), ))
    
    def clean(self):
        cleaned_data = super(Suma2, self).clean()
#        pole_nazwa = cleaned_data.get("pole_nazwa")
        pole_smiles1 = cleaned_data.get("pole_smiles1")
        pole_smiles2 = cleaned_data.get("pole_smiles2")
"""        
        if pole_nazwa == "" and pole_smiles == "":  #brak nazwy i smiles
            self.add_error('pole_nazwa','podaj dane')
        
        if pole_nazwa != "" and pole_smiles == "":  #brak smiles
            if CIRconvert(pole_nazwa)=='Did not work':
                self.add_error('pole_nazwa','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa == "" and pole_smiles != "":  #brak nazwy
            if smile_check(pole_smiles)=='it dont work':
                self.add_error('pole_smiles','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa != "" and pole_smiles != "":  #podana nazwa i smiles
            self.add_error('pole_nazwa','wszystkie pola wypełnione')

        
        if pole_nazwa2 == "" and pole_smiles2 == "":  #brak nazwy i smiles
            self.add_error('pole_nazwa','podaj dane')
        
        if pole_nazwa2 != "" and pole_smiles2 == "":  #brak smiles
            if CIRconvert(pole_nazwa2)=='Did not work':
                self.add_error('pole_nazwa','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa2 == "" and pole_smiles2 != "":  #brak nazwy
            if smile_check(pole_smiles2)=='it dont work':
                self.add_error('pole_smiles','smiles nie istnieje')
            else:
                print('Przeszlo')
                pass
        if pole_nazwa2 != "" and pole_smiles2 != "":  #podana nazwa i smiles
            self.add_error('pole_nazwa','wszystkie pola wypełnione')
"""
