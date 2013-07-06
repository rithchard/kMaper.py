"""
kMaper.py is a tool to test in dfd

"""
import Helper
'''
' Starting
'''


#urlBase =  sys.argv[1]
urlBase = 'www.thiseas-taekwondo.gr'

if urlBase.startswith('http') or urlBase.startswith('www'):
  SITE = Helper.getSITE(urlBase)
	Helper.empezando(SITE)
	Helper.checkMotor(SITE)
	Helper.getInfoJoomla(SITE)
else:
	Helper.newbie('La URL es Invalida!','Ejemplo de uso:')
	exit(1)
