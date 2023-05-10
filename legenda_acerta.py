import os
import random

limpeza_on = True
base = os.path.join(os.path.expanduser('~'), 'docker', 'plexmovies')

def lista_arquivos(a):

	os.chdir(a)
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	return files


def lista_diretorios():
	
    subfolders = [f.path for f in os.scandir(diretorio) if f.is_dir()]
    return subfolders


def main():

    diretorios=lista_diretorios()
    for a in diretorios:
        lista = lista_arquivos(a)
        is_Subs = False
        tem_legenda = False
        for b in a:
            if ("RARGB.txt" in b) or ("RARBG_DO_NOT_MIRROR.exe" in b): os.remove(b)
            if "Subs" in b: is_Subs = True
            if ".srt" in b: tem_legenda = True
            if 

        if tem_legenda: continue
        if not is_Subs: continue
        diretorio_Subs = os.path.join(a, 'Subs')
        lista2 = lista_arquivos(diretorio_Subs)





if __name__ == "__main__":
	main()
