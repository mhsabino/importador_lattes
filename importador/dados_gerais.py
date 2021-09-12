from os import listdir
from os.path import isfile, join
import re
import xml.etree.ElementTree as ET
import mysql.connector

from unicodedata import normalize

def remove_acentos(string):
	return normalize('NFKD', string).encode('ASCII','ignore').decode('ASCII')

def remove_simbolos(string):
  return re.sub(r'\W+ ', '', string)

def maiusculo(string):
  return string.upper()

def normaliza(string):
  return maiusculo(remove_acentos(remove_simbolos(string)))

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1',
                               database='lattes_db')

cursor = conn.cursor()

CURRICULOS_PATH = '/Users/msabino/projects/mateus/lattes/xmls/'

curriculos = [f for f in listdir(CURRICULOS_PATH) if isfile(join(CURRICULOS_PATH, f))]

# curriculos = [curriculos[0]]

for curriculo in curriculos:
  xml_tree = ET.parse(CURRICULOS_PATH + curriculo)

  root = xml_tree.getroot()

  dados_gerais 	  = root.find('DADOS-GERAIS')
  nome_do_docente = normaliza(dados_gerais.get('NOME-COMPLETO'))

  print('*'*20)
  print('nome_do_docente', nome_do_docente)

  cursor.execute('SELECT id_1dados_gerais FROM tab_1_dados_gerais WHERE nome_completo = %s', (nome_do_docente,))

  identificacao = 0
  row = cursor.fetchone()
  conn.commit()

  try:
    identificacao = row[0]
    print(identificacao)
    print("ERRO: O docente '{0}' já existe no banco de dados".format(nome_do_docente))
    continue

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' será inserido no banco.".format(nome_do_docente))

  pais_nascimento   = normaliza(dados_gerais.get('PAIS-DE-NASCIMENTO') or '')
  uf_nascimento     = normaliza(dados_gerais.get('UF-NASCIMENTO') or '')
  cidade_nascimento = normaliza(dados_gerais.get('CIDADE-NASCIMENTO') or '')

  try:
    cursor.execute('INSERT INTO tab_1_dados_gerais (nome_completo, pais_nascimento, uf_nascimento, cidade_nascimento) VALUES (%s, %s, %s, %s)', (nome_do_docente, pais_nascimento, uf_nascimento, cidade_nascimento))
    conn.commit()
    print('Docente inserido com sucesso!')
  except Exception as e:
    print('ERRO: Ao salvar o docente: ')
    print(e)

conn.close()