import os
import random

limpeza_on = False
# define local dos filmes
base = os.path.join(os.path.expanduser('~'), 'docker', 'plexmovies')


def lista_arquivos(a):

	os.chdir(a)
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	return files


def lista_dir_path(a):
	
    subfolders = [f.path for f in os.scandir(a) if f.is_dir()]
    return subfolders


def lista_dir(a):
	
    subfolders = [f.name for f in os.scandir(a) if f.is_dir()]
    return subfolders

def main():

    raiz=lista_dir_path(base)
    for a in raiz:
        lista = lista_arquivos(a)
        for 
        is_Subs = False
        tem_legenda = False
        for b in a:
            if ("RARGB.txt" in b) or ("RARBG_DO_NOT_MIRROR.exe" in b): 
                if limpeza_on:
                    os.remove(b)
                else:
                    print ("lixo detectado")
                continue
            if "Subs" in b: is_Subs = True
            if ".srt" in b: tem_legenda = True
            if 

        if tem_legenda: continue
        if not is_Subs: continue
        diretorio_Subs = os.path.join(a, 'Subs')
        lista2 = lista_arquivos(diretorio_Subs)





if __name__ == "__main__":
	main()
