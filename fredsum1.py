import os
import sys
from pathlib import Path
from pathlib import PurePosixPath
import hashlib
import itertools
import time


def imprime(string, codigo=''):

	class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

	if codigo == 'FAIL':
		print (bcolors.FAIL + string + bcolors.ENDC)

	elif codigo == 'WARNING':
		print (bcolors.WARNING + string + bcolors.ENDC)

	else:
		PRINT(string)

BUF_SIZE = 65536 * 2000
lista_ext_inicial = ['.bin', '.avi', '.mkv', '.mp4', '.iso', '.fre', '.vob', '.gba', '.3ds']
lista_ext =[]

for a in lista_ext_inicial:
	lista_ext.append(a.lower())
	lista_ext.append(a.upper())

# flag para ligar modo de teste
modo_teste = False

arquivo_output = '# FREDSUM CHECKSUM CHECKER\n# Usage: fredsum config_file\n'
arquivo_output += '# Use Linux-style path \n'
if modo_teste: lista_ext.append('.py')

def hash_file (filepath):

	a = filepath.split('/')

	a = [y for y in a if y]

	f = Path.cwd().joinpath(*a)
	sha1 = hashlib.sha1()

	*arg, name = a
	print ('> ' + name)

	try:
		with f.open('rb') as file:
			while True:
				data = file.read(BUF_SIZE)
				if not data:
					break
				sha1.update(data)
	except:
		imprime ('      [ERROR] ' + filepath + ' -> not found.', 'FAIL')
		return('')

	return (sha1.hexdigest())


def devolve_arquivos_hasheados(arquivo):

	lista = []

	for x in arquivo:
		if (x[:2] == 'd=' or x[:2] == '# ' or x[:2] == '% '):
			continue
		else:
			lista.append (x.split('; '))
		if not len(x.split('; ')) == 4:
			print ("\nError in config file")
			exit(1)

	return (lista)


def devolve_lista_dirs(arquivo):

	return ([y[2:] for y in arquivo if 'd=' in y])


def check_duplicates(lista):

	s=set(lista)
	d=[]
	for x in lista:
		if x in s:
			s.remove(x)
		else:
			if '.VOB' in x:
				pass
			else:
				d.append(x)
	return(d)

def retorna_repetidos(lista, repetidos, coluna):
	saida = []
	for a in repetidos:
		for b in lista:
			if (a == b[coluna]):
				saida.append(b)
	return(saida)

def obtem_listaarquivos_atual(lista_dir):

	lista_arquivos = []

	for dir in (lista_dir):
		p = Path(dir)
		if p.exists():
			for ext in lista_ext:
				for i in p.rglob('*' + ext):
					if ';' not in str(i):
						lista_arquivos.append((i.name, str(PurePosixPath(i)),
						                       str(i.stat().st_size)))
					else:
						print ('\nFilename contains ; :' + str(i))
						exit(1)
		else:
			print ('\nPath ' + dir + ' does not exist!')
			exit(1)
	return (lista_arquivos)


def retorna_arquivos_faltantes (lista_arquivos_original, lista_arquivos_atual):

	arquivos_faltantes_comdiretorios = []

	set_atual = set([row[1] for row in lista_arquivos_atual])

	for a in range(len(lista_arquivos_original)):
		if lista_arquivos_original[a][1] in set_atual:
			set_atual.remove(lista_arquivos_original[a][1])

	lista_atual = list (set_atual)

	for a in lista_arquivos_atual:
		for b in lista_atual:
			if a[1] == b:
				arquivos_faltantes_comdiretorios.append(a)

	return (arquivos_faltantes_comdiretorios)

def grava_arquivo(string, arquivo):

	if len(string) > 5:
		with open(arquivo, "w", encoding='utf-8') as f:
			f.write(string)

def retorna_hashes_dos_faltantes(lista):

	lista_completa = []
	bytes_lido = 0

	t0 = time.time()

	hash_list = [hash_file(row[1]) for row in lista]

	t1 = time.time()

	for a in range (len(lista)):


		lista_completa.append((lista[a][0],
							   lista[a][1],
							   lista[a][2],
							   hash_list[a]))

	for a in lista_completa:
		bytes_lido += int(a[2])

	mega_lido = bytes_lido / 1024 ** 2

	speed = mega_lido / (t1-t0)

	return (lista_completa, speed)

def func_apenasteste(lista_arquivos_original, search_string):

	teste=[]

	for a in lista_arquivos_original:
			if search_string.lower() in a[0].lower():
				teste.append(a)

	if len(teste)==0:
		print('\nNo file meets criteria')
		exit(1)

	for a in teste:
		print(a[0])

	a = input('Would you like to check the above? ')

	if (a == 'y' or a == 'Y'):

		for a in teste:
			hash = hash_file(a[1])
			if hash:
				if not a[3] == hash:
					imprime ('      [ERROR] ' + a[1] + ' -> HASH ERROR!', 'WARNING')


def main():

	nomes_dos_arquivos =[]
	global arquivo_output
	problem = False
	apenas_teste = False
	search_string = ''

	if len(sys.argv) == 1:
		print('Fredsum 1.0')
		print('Usage: fredsum config_file                       -> Search and add new files')
		print(  '               config_file [-t] [filename]       -> Check all files or filname')
		exit(0)

	try:
		arquivo_conf_nome = sys.argv[1]
		f = open(arquivo_conf_nome, "r", encoding='utf-8')
		arquivo_conf_original = [line.strip().strip(';') for line in f]
		arquivo_conf_original = [y for y in arquivo_conf_original if y]
	except:
		print ('\nConfiguration file not found!\n')
		exit(1)

	if len (arquivo_conf_original) < 1:
		print("\nConfig file corrupted")
		exit(1)

	if len(sys.argv) > 2:
		if sys.argv[2] == '-t' or sys.argv[2] == '-T':
			apenas_teste = True
		else:
			print('\nUnknown command')
			exit(1)

		try:
			search_string = sys.argv[3]
		except:
			pass

		if search_string == '':
			print('\nA search string is necessary')
			exit(1)

	lista_dir_original = devolve_lista_dirs(arquivo_conf_original)

	lista_arquivos_original = devolve_arquivos_hasheados(arquivo_conf_original)

	if apenas_teste:
		func_apenasteste(lista_arquivos_original, search_string)
		exit(0)

	lista_arquivos_atual = obtem_listaarquivos_atual(lista_dir_original)

	arquivos_faltantes = retorna_arquivos_faltantes \
	                          (lista_arquivos_original, lista_arquivos_atual)

	for a in lista_dir_original:
		string = '\n' + 'd=' + a
		arquivo_output += string

	arquivo_output += '\n'

	for a in arquivo_conf_original:
		if a[:2] == '% ':
			arquivo_output += '\n' + a

	arquivo_output += '\n'

	if arquivos_faltantes:

		[print(x[1]) for x in arquivos_faltantes]

		if not modo_teste:
			yu = input('The above files are not hashed. Would you like ' +
			       'to include them? (y/n) ')
		else:
			print ('arquivos faltantes!')
			yu = 'y'

		if (yu == 'y' or yu == 'Y'):

			a, b, c = zip(*lista_arquivos_atual)

			nomes_repetidos = check_duplicates(a)

			if nomes_repetidos:
				arquivo_output += "\n\n# Name duplicates:\n"
				repetidos = retorna_repetidos(lista_arquivos_original,
														nomes_repetidos, 0)
				for x in repetidos:
					arquivo_output += '# ' + '; '.join(x) + '\n'

			for a in lista_arquivos_original:
				arquivo_output += '\n'
				for b in range(len(lista_arquivos_original[0])):
					arquivo_output += a[b]
					if b < len(lista_arquivos_original[0]):
						arquivo_output += '; '

			arquivo_output += '\n\n# Newly add:'

			arquivos_faltantes, speed = retorna_hashes_dos_faltantes (arquivos_faltantes)

			for a in arquivos_faltantes:
				arquivo_output += '\n'
				for b in range(len(arquivos_faltantes[0])):
					arquivo_output += a[b]
					if b < len(arquivos_faltantes[0]):
						arquivo_output += '; '

			if speed > 0.06:
				print ('\n' + '%.1f' % speed + ' MB/sec\n')

			grava_arquivo(arquivo_output, arquivo_conf_nome)
			exit(0)

	else:

		if not modo_teste:
			print('No new files found.')
			yu = input('Would you like to check everything? ')
		else:
			yu = 'y'

		if not (yu == 'y' or yu == 'Y'):
			exit(0)

		else:

			for a in lista_arquivos_original:

				hash = hash_file (a[1])

				if hash:
					if not a[3].strip('; ') == hash:
						imprime ('      [ERROR] ' + a[1] + ' -> HASH ERROR!', 'WARNING')
						arquivo_output += '\n\n# [ERROR]\n# ' + a[1] + '; ' + hash_file(a[1])  + " -> actual hash!"
						arquivo_output += '\n# ' + a[1] + '; ' + a[3]  + " -> old hash\n"
						problem = True

			a, b, c, d = zip(*lista_arquivos_original)

			nomes_repetidos = check_duplicates(a)

			hashes_repetidas = check_duplicates(d)

			if nomes_repetidos:
				arquivo_output += "\n# Name duplicates:\n"
				repetidos = retorna_repetidos(lista_arquivos_original,
														nomes_repetidos, 0)
				for x in repetidos:
					arquivo_output += '# ' + '; '.join(x) + '\n'

			if hashes_repetidas:
				arquivo_output += "\n# Hash duplicates:\n"
				repetidos = retorna_repetidos(lista_arquivos_original,
													 hashes_repetidas, 3)
				for x in repetidos:
					arquivo_output += '# '
					arquivo_output += '; '.join(x)
					arquivo_output += '\n'

			for a in lista_arquivos_original:
				arquivo_output += '\n'
				for b in range(len(lista_arquivos_original[0])):
					arquivo_output += a[b]
					if b < len(lista_arquivos_original[0]):
						arquivo_output += '; '

			#print (arquivo_output)
			if (problem or nomes_repetidos or hashes_repetidas):
				grava_arquivo (arquivo_output, arquivo_conf_nome)
				exit(0)
			else:
				print('\n All hashes ok, no duplicates\n')
				exit(0)

if __name__ == "__main__": main()

