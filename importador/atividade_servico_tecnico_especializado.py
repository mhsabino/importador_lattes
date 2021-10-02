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

        atividades_de_servico_tecnico_especializado = atuacao_profissional.find('ATIVIDADES-DE-SERVICO-TECNICO-ESPECIALIZADO')

        if atividades_de_servico_tecnico_especializado != None:

          servicos_tecnico_especializado = atividades_de_servico_tecnico_especializado.findall('SERVICO-TECNICO-ESPECIALIZADO')

          for  servico_tecnico_especializado in servicos_tecnico_especializado:

            ano_inicio        = texto.normaliza(servico_tecnico_especializado.get('ANO-INICIO') or '')
            ano_fim           = texto.normaliza(servico_tecnico_especializado.get('ANO-FIM') or '')
            nome_orgao        = texto.normaliza(servico_tecnico_especializado.get('NOME-ORGAO') or '')
            nome_unidade      = texto.normaliza(servico_tecnico_especializado.get('NOME-UNIDADE') or '')
            servico_realizado = texto.normaliza(servico_tecnico_especializado.get('SERVICO-REALIZADO') or '')
            nome_instituicao  = texto.normaliza(atuacao_profissional.get('NOME-INSTITUICAO') or '')

            try:
              cursor.execute('INSERT INTO tab_8_serviço_tecnico_especializado (docente, nome_instituicao, ano_inicio, ano_fim, nome_orgao, nome_unidade, servico_realizado, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, nome_instituicao, ano_inicio, ano_fim, nome_orgao, nome_unidade, servico_realizado, identificacao))
              conexao.conn.commit()
              print('Servico tecnico especializado {0} inserido com sucesso!'.format(nome_instituicao))
            except Exception as e:
              print('ERRO: Ao salvar o Servico tecnico especializado {0}: '.format(nome_instituicao))
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()