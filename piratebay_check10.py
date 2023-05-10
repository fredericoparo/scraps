# -*- coding: utf-8 -*-

import sys
import os
import urllib.request
import pickle
from bs4 import BeautifulSoup
import webbrowser
import operator
import subprocess
import datetime
import io
import gzip



filmes_tag = ["dvdrip", "bdrip", "xvid", "x264", "ac3", "720p", "1080p", "dvdscr", '1cdrip', 'brrip', 'hdrip']
tranqueira = set([" hindi ", " cam ", " ts "])
extensions = set(['XXX', 'WWE.', 'Anal. ', 'Fuck. ', 'Brazzers', 'Cock', 'Casting'])

url = "http://thepiratebay.org/top/all"

adicoes = []
total_db=0
picke_file = 'pickle.pck'

class Contem:
	def __init__(self):
		self.titulo = ""
		self.link = ""
		self.tipo = ""
		self.atencao = False
		self.telesync = False
		self.marcado = False
		self.idade = ""


def le_historico():
	''' Lê arquivo pickle '''

	arquivo=[]

	if os.path.isfile(picke_file):

		with open(picke_file, "rb") as file:
			arquivo = pickle.load(file)

	else:

		print('Pickle não encontrado')

	return(arquivo)


def le_filmes_corta():
	''' carrega lista de textos a ser desconsiderados '''

	arquivo=[]

	with open("filmes_corta.txt", "r") as f:
		arquivo = [line.strip().lower() for line in f]
		arquivo = [y for y in arquivo if y]

	return(list(set(arquivo)))


def le_atencao():
	''' lista de itens que devem ser destacados '''

	arquivo=[]

	with open("atencao.txt", "r") as f:
		arquivo = [line.strip().lower() for line in f]
		arquivo = [y for y in arquivo if y]

	return(list(set(arquivo)))


def grava(lista):
	global total_db

	with open(picke_file, "wb") as file:
		pickle.dump(lista, file)

	total_db = len(lista)


def le_web():

	with open("web.html", "r") as f:
		string = f.read()

	return(string)


def grava_web(string):

	with open("web_out.html", "w") as f:
		f.write(string)


def abre_pirate():

		texto = ""
		try:
			request = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", "Accept-Encoding": "gzip"} ))
			texto = request.read()
			#request = urllib.request.urlopen(urllib.request.Request(url[:(len(url)-3)]+"48hall", headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", "Accept-Encoding": "gzip"} ))
			#texto = request.read()

		except:
			try:
				request = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", "Accept-Encoding": "gzip"} ))
				texto = request.read()
			except:
				print("\nPirateBay down!\n")

			return(texto)


		try:
			bi = io.BytesIO(texto)
			gf = gzip.GzipFile(fileobj=bi, mode="rb")
			return(gf.read())

		except:
			print("\nGzip falhou\n!")
			return(texto)


def categoriza():

	importante_tag = le_atencao()

	for i in adicoes:

		top = False

		i.titulo = i.titulo.replace(".", " ")
		i.titulo = i.titulo.replace("mp4", "")

		a1 = i.titulo.find('[')
		a2 = i.titulo.find(']')

		if a1 > 0 and a2 > 0:
				if a2 - a1 < 17:
						i.titulo = i.titulo.replace(i.titulo[a1:a2+1], "")

		i.titulo = i.titulo.strip()

		for e in range(10, 30):
				if("S" + str(e) + "E") in i.titulo:
						i.tipo = "serie"
						top = True
						break
		else:
				if "S0" in i.titulo:
						start = i.titulo.find("S0")
						if (i.titulo[start+1:start+3].isdigit() and i.titulo[start+3:start+4]=="E" and i.titulo[start+4:start+6].isdigit()):
								i.tipo = "serie"
								top = True
								continue

		if not top:
			for d in filmes_tag:
				if d in i.titulo.lower():
					if any(word in i.titulo.lower() for word in tranqueira):
						#i.titulo = " ".join(["[TeleSync]", i.titulo])
						i.telesync = True
						i.tipo = "outros"
						break
					else:
						i.tipo = "filme"
						break
			else:
				i.tipo = "outros"


	for d in importante_tag:
		for i in adicoes:
			if d in i.titulo.lower():
				#i.titulo = " ".join(["(!)", i.titulo])
				i.atencao = True
				continue


def imprime_temp():
	for i in adicoes:
		fire = i.tipo + ' * ' + i.titulo
		if i.atencao == True: fire=fire + ' * atencao '
		if i.telesync == True: fire=fire + ' * telesync'
		print(fire)


def imprime():

	global adicoes, total_db
	filmes, series, outros, alternativos = "", "", "", ""
	string = le_web()
	flag = False

	lista_de_titulos = [i.titulo for i in adicoes]

	zipped = zip(lista_de_titulos, adicoes)
	zipped = sorted(list(zipped), key = operator.itemgetter(0))
	lista_de_titulos, adicoes = zip(*zipped)

	for i in adicoes:

		if i.atencao:
			i.titulo = '<b>' + i.titulo + '</b>'

	''' Idade removida

		if "Today" in i.idade:

			i.titulo = '*** ' + i.titulo

		else:

			if not "Y-day" in i.idade:
				a = i.idade.strip("( )")
				today = datetime.date.today()
				ano = int(datetime.date.today().strftime("%Y"))

				try:
					mes = int(a[0:2])
					dia = int(a[3:5])


				except:
					mes=0
					dia=0

				data_torrent = datetime.date(ano, mes, dia)
				tempototal = today - data_torrent

				if tempototal.days < 0:
					data_torrent = datetime.date((ano-1), mes, dia)
					tempototal = today - data_torrent
					i.idade = ' (' + str(tempototal.days) + ' days)'

				elif tempototal.days == 1:
					i.idade = ' (Y-day)'

				else:
					i.idade = ' (' + str(tempototal.days) + ' days)'

	'''

	for i in adicoes:
		if i.marcado: continue

		for x in adicoes:
			if not i.titulo == x.titulo: continue
			if flag:
				alternativos += '&nbsp;<a href="' + x.link + '" target="_blank">' + '(alt)</a>'
				x.marcado = True
			else:
				flag = True

		if i.tipo == 'filme':
			google_keys = (i.titulo.lower().replace('-',' ').replace('_',' ')).split(" ")

			lista_do_corta = filmes_tag + le_filmes_corta()

			for o in lista_do_corta:
				if o in google_keys:
					google_keys.remove(o)

			google_keys = [y for y in google_keys if y] #retira itens vazios da lista

			googlequery  = '&nbsp;<a href="' + 'http://google.com/search?btnI=1&q='
			googlequery += '+'.join(google_keys[:3]) + '+movie' + '" target="_blank">' + '(google)</a>'
			filmes += '<p><a href="' + i.link +'" target="_blank">' + i.titulo +'</a>' + i.idade + alternativos + googlequery + '</p>'

		elif i.tipo == 'serie':
			series += '<p><a href="' + i.link +'" target="_blank">' + i.titulo +'</a>' + i.idade + alternativos + '</p>'

		else:
			outros += '<p><a href="' + i.link +'" target="_blank">' + i.titulo +'</a>'+ i.idade + alternativos + '</p>'

		alternativos = ""
		flag = False


	if filmes: string = string.replace('<!--###filmes###-->', '<h1>/// Filmes</h1>' + filmes)
	if series: string = string.replace('<!--###series###-->', '<h1>/// S&eacute;ries</h1>' + series)
	if outros: string = string.replace('<!--###outros###-->', '<h1>/// Outros</h1>' + outros)

	string = string.replace('<h2>all your bases are belong to us</h2>', '<h2>all your bases are belong to us /// (' + str(total_db) + ') docs in db</h2>')
	#http://www.imdb.com/find?q=teste+2012&s=tt
	#http://www.youtube.com/results?search_query=fred+trailer

	if adicoes:
		grava_web(string)


def main():

		lista=[]


		loriginal = le_historico()

		pagina = abre_pirate()

		if not pagina:
			sys.exit("\nDeu pau\n")

		soup = BeautifulSoup(pagina, "html.parser")

		pagina_text = pagina.decode("utf-8", "replace")

		lista_link = soup.find_all("a",{ "class" : "detLink" })

		for item in lista_link:
			alfa = Contem()
			human = str(item.encode("ascii"))
			start = human.find("\">") + 2
			end = human.find("</a>", start)
			if not any (ext in human[start:end] for ext in extensions):
				if human[start:end] not in loriginal:
					lista.append(human[start:end])
					alfa.titulo = human[start:end]
					start_a = human.find("href=\"") + 6
					end_a = human.find("\" title")
					# Se for .se tem que mudar para [0:22] abaixo
					alfa.link = url[0:23] + human[start_a:end_a]
					start_b = pagina_text.find(human[start_a+1:end_a])
					end_b = start_b + len(human[start_a:end_a])
					#iidade = pagina_text.find(">Uploaded ", end_b) + 10
					#alfa.idade = ' (' + pagina_text[iidade:iidade + 5] + ') '
					#print(pagina_text[iidade:iidade + 5])
					adicoes.append(alfa)


		if lista:
			grava(lista + loriginal)
			categoriza()
			imprime()
			webbrowser.open('web_out.html')
			#webbrowser.get(using='chrome').open(web_out.html,new=new)


		else:
			print("\nNenhum arquivo novo!")
			escolha = input("\nCarregar último web_out? ")
			if escolha =='s' or escolha =='y':
				webbrowser.open('web_out.html')


			if escolha =='d': os.remove("pickle.pck")



if __name__ == "__main__":
	main()
