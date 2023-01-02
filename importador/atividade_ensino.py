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

        atividades_de_ensino = atuacao_profissional.find('ATIVIDADES-DE-ENSINO')

        if atividades_de_ensino != None:

          ensinos = atividades_de_ensino.findall('ENSINO')

          for  ensino in ensinos:

            ano_inicio       = texto.normaliza(ensino.get('ANO-INICIO') or '')
            ano_fim          = texto.normaliza(ensino.get('ANO-FIM') or '')
            flag_periodo     = texto.normaliza(ensino.get('FLAG-PERIODO') or '')
            tipo_ensino      = texto.normaliza(ensino.get('TIPO-ENSINO') or '')

            disciplinas = ensino.findall('DISCIPLINA')

            sequencias = []

            for disciplina in disciplinas:
              sequencias.append(disciplina.text)

            campo_sequencias = [''] * 130

            for index, sequencia in enumerate(sequencias):
              campo_sequencias[index] = sequencia

            try:
              cursor.execute("""INSERT INTO tab_7_ensino 
                            (docente, flag_periodo, tipo_ensino, ano_inicio, ano_fim, disciplina_sequencia_especificacao1, disciplina_sequencia_especificacao2, disciplina_sequencia_especificacao3, disciplina_sequencia_especificacao4, disciplina_sequencia_especificacao5, disciplina_sequencia_especificacao6, disciplina_sequencia_especificacao7, disciplina_sequencia_especificacao8, disciplina_sequencia_especificacao9, disciplina_sequencia_especificacao10, disciplina_sequencia_especificacao11, disciplina_sequencia_especificacao12, id_1dados_gerais) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                            (nome_do_docente, flag_periodo, tipo_ensino, ano_inicio, ano_fim, campo_sequencias[0], campo_sequencias[1], campo_sequencias[2], campo_sequencias[3], campo_sequencias[4], campo_sequencias[5], campo_sequencias[6], campo_sequencias[7], campo_sequencias[8], campo_sequencias[9], campo_sequencias[10], campo_sequencias[11], identificacao))
              conexao.conn.commit()
              print('Ensino {0} inserido com sucesso!'.format(sequencia))
            except Exception as e:
              print('ERRO: Ao salvar o Ensino {0}: '.format(sequencia))
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
