import re
from unicodedata import normalize

def remove_acentos(string):
	return normalize('NFKD', string).encode('ASCII','ignore').decode('ASCII')

def remove_simbolos(string):
  return re.sub(r'\W+ ', '', string)

def maiusculo(string):
  return string.upper()

def normaliza(string):
  return maiusculo(remove_acentos(remove_simbolos(string)))
