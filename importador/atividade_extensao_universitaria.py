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
    
    atuacoes_profissionais_grupo = dados_gerais.find('ATUACOES-PROFISSIONAIS')

    if atuacoes_profissionais_grupo != None:

      atuacoes_profissionais = atuacoes_profissionais_grupo.findall('ATUACAO-PROFISSIONAL')

      for atuacao_profissional in atuacoes_profissionais:

        atividades_de_extensao_universitaria = atuacao_profissional.find('ATIVIDADES-DE-EXTENSAO-UNIVERSITARIA')

        if atividades_de_extensao_universitaria != None:

          extensoes = atividades_de_extensao_universitaria.findall('EXTENSAO-UNIVERSITARIA')

          for extensao in extensoes:

            ano_inicio                      = texto.normaliza(extensao.get('ANO-INICIO') or '')
            ano_fim                         = texto.normaliza(extensao.get('ANO-FIM') or '')
            nome_orgao                      = texto.normaliza(extensao.get('NOME-ORGAO') or '')
            nome_unidade                    = texto.normaliza(extensao.get('NOME-UNIDADE') or '')
            atividade_de_extensao_realizada = texto.normaliza(extensao.get('ATIVIDADE-DE-EXTENSAO-REALIZADA') or '')

            try:
              cursor.execute('INSERT INTO tab_9_atividade_extensao_universitaria (docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, atividade_extensao_realizada) VALUES (%s, %s, %s, %s, %s, %s)', (nome_do_docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, atividade_de_extensao_realizada))
              conexao.conn.commit()
              print('Extensao inserida com sucesso!')
            except Exception as e:
              print('ERRO: Ao salvar a Extensao {0}: ')
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()