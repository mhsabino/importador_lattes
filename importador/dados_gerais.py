from os import listdir
from os.path import isfile, join

import modulos.normalizacao as texto
import modulos.conexao_banco as conexao
import modulos.xml_parse as xml

cursor = conexao.conn.cursor()

curriculos = [f for f in listdir(xml.CURRICULOS_PATH) if isfile(join(xml.CURRICULOS_PATH, f))]

for curriculo in curriculos:
  xml_tree = xml.ET.parse(xml.CURRICULOS_PATH + curriculo)

  root = xml_tree.getroot()

  dados_gerais 	  = root.find('DADOS-GERAIS')
  nome_do_docente = texto.normaliza(dados_gerais.get('NOME-COMPLETO'))

  print('*'*20)
  print('nome_do_docente', nome_do_docente)

  cursor.execute('SELECT id_1dados_gerais FROM tab_1_dados_gerais WHERE nome_completo = %s', (nome_do_docente,))

  identificacao = 0
  row = cursor.fetchone()
  conexao.conn.commit()

  try:
    identificacao = row[0]
    print(identificacao)
    print("ERRO: O docente '{0}' já existe no banco de dados".format(nome_do_docente))
    continue

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' será inserido no banco.".format(nome_do_docente))

  pais_nascimento   = texto.normaliza(dados_gerais.get('PAIS-DE-NASCIMENTO') or '')
  uf_nascimento     = texto.normaliza(dados_gerais.get('UF-NASCIMENTO') or '')
  cidade_nascimento = texto.normaliza(dados_gerais.get('CIDADE-NASCIMENTO') or '')

  try:
    cursor.execute('INSERT INTO tab_1_dados_gerais (nome_completo, pais_nascimento, uf_nascimento, cidade_nascimento) VALUES (%s, %s, %s, %s)', (nome_do_docente, pais_nascimento, uf_nascimento, cidade_nascimento))
    conexao.conn.commit()
    print('Docente inserido com sucesso!')
  except Exception as e:
    print('ERRO: Ao salvar o docente: ')
    print(e)

conexao.conn.close()