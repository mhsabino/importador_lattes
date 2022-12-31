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
    
    idiomas_grupo = dados_gerais.find('IDIOMAS')

    if idiomas_grupo != None:

      idiomas = idiomas_grupo.findall('IDIOMA')

      for idioma in idiomas:

        descricao = texto.normaliza(idioma.get('DESCRICAO-DO-IDIOMA') or '')

        try:
          cursor.execute('INSERT INTO tab_13_idioma (docente, descricao_do_idioma1, id_1dados_gerais) VALUES (%s, %s, %s)', (nome_do_docente, descricao, identificacao))
          conexao.conn.commit()
          print('Idioma inserido com sucesso!')
        except Exception as e:
          print('ERRO: Ao salvar o Idioma')
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
