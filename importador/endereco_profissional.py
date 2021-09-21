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

curriculos = [curriculos[0]]

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
    
    endereco = dados_gerais.find('ENDERECO')

    if endereco != None:
      endereco_profissional = endereco.find('ENDERECO-PROFISSIONAL')

      if endereco_profissional != None:
        nome_instituicao_empresa = normaliza(endereco_profissional.get('NOME-INSTITUICAO-EMPRESA') or '')
        nome_orgao               = normaliza(endereco_profissional.get('NOME-ORGAO') or '')
        nome_unidade             = normaliza(endereco_profissional.get('NOME-UNIDADE') or '')
        pais                     = normaliza(endereco_profissional.get('PAIS') or '')
        uf                       = normaliza(endereco_profissional.get('UF') or '')
        cidade                   = normaliza(endereco_profissional.get('CIDADE') or '')

        try:
          cursor.execute('INSERT INTO tab_2_endereco_profissional (docente, nome_instituicao_empresa, nome_orgao, nome_unidade, pais, uf, cidade, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, nome_instituicao_empresa, nome_orgao, nome_unidade, pais, uf, cidade, identificacao))
          conn.commit()
          print('Endereco inserido com sucesso!')
        except Exception as e:
          print('ERRO: Ao salvar o Endereco: ')
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conn.close()