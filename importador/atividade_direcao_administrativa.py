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

        atividades_de_direcao_e_administracao = atuacao_profissional.find('ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO')


        if atividades_de_direcao_e_administracao != None:

          direcao_e_administracoes = atividades_de_direcao_e_administracao.findall('DIRECAO-E-ADMINISTRACAO')

          for  direcao_e_administracao in direcao_e_administracoes:

            ano_inicio       = texto.normaliza(direcao_e_administracao.get('ANO-INICIO') or '')
            ano_fim          = texto.normaliza(direcao_e_administracao.get('ANO-FIM') or '')
            nome_orgao       = texto.normaliza(direcao_e_administracao.get('NOME-ORGAO') or '')
            cargo_ou_funcao  = texto.normaliza(direcao_e_administracao.get('CARGO-OU-FUNCAO') or '')
            nome_unidade     = texto.normaliza(direcao_e_administracao.get('NOME-UNIDADE') or '')

            try:
              cursor.execute('INSERT INTO tab_5_atividade_direcao_administracao (docente, ano_inicio, ano_fim, nome_orgao, cargo_ou_funcao, nome_unidade, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, ano_inicio, ano_fim, nome_orgao, cargo_ou_funcao, nome_unidade, identificacao))
              conexao.conn.commit()
              print('Atividade Direcao {0} inserida com sucesso!'.format(cargo_ou_funcao))
            except Exception as e:
              print('ERRO: Ao salvar a Atividade Direcao {0}: '.format(cargo_ou_funcao))
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
