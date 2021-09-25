from os import listdir
from os.path import isfile, join

import modulos.normalizacao as texto
import modulos.conexao_banco as conexao
import modulos.xml_parse as xml

cursor = conexao.conn.cursor()

curriculos = [f for f in listdir(xml.CURRICULOS_PATH) if isfile(join(xml.CURRICULOS_PATH, f))]

# curriculos = [curriculos[0]]

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

        nome_instituicao = texto.normaliza(atuacao_profissional.get('NOME-INSTITUICAO') or '')

        vinculos = atuacao_profissional.findall('VINCULOS')

        for vinculo in vinculos:
          tipo_de_vinculo                         = texto.normaliza(vinculo.get('TIPO-DE-VINCULO') or '')
          flag_dedicacao_exclusiva                = texto.normaliza(vinculo.get('FLAG-DEDICACAO-EXCLUSIVA') or '')
          ano_inicio                              = texto.normaliza(vinculo.get('ANO-INICIO') or '')
          ano_fim                                 = texto.normaliza(vinculo.get('ANO-FIM') or '')
          flag_vinculo_empregaticio               = texto.normaliza(vinculo.get('FLAG-VINCULO-EMPREGATICIO') or '')
          outro_vinculo_informado                 = texto.normaliza(vinculo.get('OUTRO-VINCULO-INFORMADO') or '')
          outro_enquadramento_funcional_informado = texto.normaliza(vinculo.get('OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO') or '')
          outras_informacoes                      = texto.normaliza(vinculo.get('OUTRAS-INFORMACOES') or '')

          try:
            cursor.execute('INSERT INTO tab_4_atuacoes_profissionais (docente, nome_instituicao, tipo_de_vinculo, flag_dedicacao_esclusiva, ano_inicio, ano_fim, flag_vinculo_empregaticio, outro_vinculo_informado, outro_enquadramento_funcional_informado, outras_informacoes, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, nome_instituicao, tipo_de_vinculo, flag_dedicacao_exclusiva, ano_inicio, ano_fim, flag_vinculo_empregaticio, outro_vinculo_informado, outro_enquadramento_funcional_informado, outras_informacoes, identificacao))
            conexao.conn.commit()
            print('Atuacao profissional {0} inserida com sucesso!'.format(tipo_de_vinculo))
          except Exception as e:
            print('ERRO: Ao salvar a Atuacao profissional {0}: '.format(tipo_de_vinculo))
            print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()