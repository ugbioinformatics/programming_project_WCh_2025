import os

def systemcheck():
    folder_nadrzedny = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sciezka_do_pliku = os.path.join(folder_nadrzedny, "system.txt")
    with open(sciezka_do_pliku, 'r') as file:
        system = file.readline().strip()
        if system == 'Windows':
            plik = 'bat'
            splash = '\\'
        else:
            plik = 'sh'
            splash = '/'
    return plik, splash