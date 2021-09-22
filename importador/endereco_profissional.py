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
    
    endereco = dados_gerais.find('ENDERECO')

    if endereco != None:
      endereco_profissional = endereco.find('ENDERECO-PROFISSIONAL')

      if endereco_profissional != None:
        nome_instituicao_empresa = texto.normaliza(endereco_profissional.get('NOME-INSTITUICAO-EMPRESA') or '')
        nome_orgao               = texto.normaliza(endereco_profissional.get('NOME-ORGAO') or '')
        nome_unidade             = texto.normaliza(endereco_profissional.get('NOME-UNIDADE') or '')
        pais                     = texto.normaliza(endereco_profissional.get('PAIS') or '')
        uf                       = texto.normaliza(endereco_profissional.get('UF') or '')
        cidade                   = texto.normaliza(endereco_profissional.get('CIDADE') or '')

        try:
          cursor.execute('INSERT INTO tab_2_endereco_profissional (docente, nome_instituicao_empresa, nome_orgao, nome_unidade, pais, uf, cidade, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, nome_instituicao_empresa, nome_orgao, nome_unidade, pais, uf, cidade, identificacao))
          conexao.conn.commit()
          print('Endereco inserido com sucesso!')
        except Exception as e:
          print('ERRO: Ao salvar o Endereco: ')
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()