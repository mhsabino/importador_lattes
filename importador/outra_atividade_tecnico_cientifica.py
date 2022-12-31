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

        outras_atividades_cientificas = atuacao_profissional.find('OUTRAS-ATIVIDADES-TECNICO-CIENTIFICA')

        if outras_atividades_cientificas != None:

          outras_atividades = outras_atividades_cientificas.findall('OUTRA-ATIVIDADE-TECNICO-CIENTIFICA')

          for outra_atividade in outras_atividades:

            ano_inicio          = texto.normaliza(outra_atividade.get('ANO-INICIO') or '')
            ano_fim             = texto.normaliza(outra_atividade.get('ANO-FIM') or '')
            nome_orgao          = texto.normaliza(outra_atividade.get('NOME-ORGAO') or '')
            nome_unidade        = texto.normaliza(outra_atividade.get('NOME-UNIDADE') or '')
            flag_periodo        = texto.normaliza(outra_atividade.get('FLAG-PERIODO') or '')
            atividade_realizada = texto.normaliza(outra_atividade.get('ATIVIDADE-REALIZADA') or '')

            try:
              cursor.execute('INSERT INTO tab_11_outra_atividade_tecnico_cientifica (docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, flag_periodo, atividade_realizada, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, flag_periodo, atividade_realizada, identificacao))
              conexao.conn.commit()
              print('Outra atividade inserida com sucesso!')
            except Exception as e:
              print('ERRO: Ao salvar a Outra atividade {0}: ')
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
