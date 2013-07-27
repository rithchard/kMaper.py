"""
kMaper.py is a tool to test in cms's


"""
import Helper,sys
'''
' Usar: $ python kMaper.py http://www.splatgore.de/index.php
'''


urlBase =  sys.argv[1]
#urlBase = 'www.thiseas-taekwondo.gr'
#urlBase = 'http://www.rcv-reichenbach.net/index.php?option=com_mytube&view=videos&Itemid=94'
#urlBase = 'http://www.splatgore.de/index.php'
#urlBase = 'http://www.johnled.gr/index.php'
#urlBase = 'http://www.diegos-canela.de/index.php'

if urlBase.startswith('http') or urlBase.startswith('www'):
	SITE = Helper.getSITE(urlBase)
	Helper.empezando(SITE)
	Helper.checkIfJoomla(SITE)
else:
	Helper.newbie('La URL es Invalida!','Ejemplo de uso:')
	exit(1)

