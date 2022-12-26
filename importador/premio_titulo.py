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
    
    premio_grupo = dados_gerais.find('PREMIOS-TITULOS')

    if premio_grupo != None:

      premios = premio_grupo.findall('PREMIO-TITULO')

      for premio in premios:

        nome_do_premio_ou_titulo   = texto.normaliza(premio.get('NOME-DO-PREMIO-OU-TITULO') or '')
        nome_da_entidade_promotora = texto.normaliza(premio.get('NOME-DA-ENTIDADE-PROMOTORA') or '')
        ano_da_premiacao           = texto.normaliza(premio.get('ANO-DA-PREMIACAO') or '')

        try:
          cursor.execute('INSERT INTO tab_14_premio_titulos (docente, nome_do_titulo_ou_premio1, nome_da_entidade_promotora1, ano_da_premiacao1) VALUES (%s, %s, %s, %s)', (nome_do_docente, nome_do_premio_ou_titulo, nome_da_entidade_promotora, ano_da_premiacao))
          conexao.conn.commit()
          print('Premio inserido com sucesso!')
        except Exception as e:
          print('ERRO: Ao salvar o Premio')
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()