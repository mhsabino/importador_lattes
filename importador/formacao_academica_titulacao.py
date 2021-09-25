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

    formacao_academica_titulacao = dados_gerais.find('FORMACAO-ACADEMICA-TITULACAO')

    if formacao_academica_titulacao != None:
      graduacao = formacao_academica_titulacao.find('GRADUACAO')

      if graduacao != None:
        titulacao                                = 'GRADUACAO'
        titulo_do_trabalho_de_conclusao_de_curso = texto.normaliza(graduacao.get('TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO') or '')
        nome_do_orientador                       = texto.normaliza(graduacao.get('NOME-DO-ORIENTADOR') or '')
        nome_instituicao                         = texto.normaliza(graduacao.get('NOME-INSTITUICAO') or '')
        nome_curso                               = texto.normaliza(graduacao.get('NOME-CURSO') or '')
        ano_de_inicio                            = graduacao.get('ANO-DE-INICIO') or ''
        ano_de_conclusao                         = graduacao.get('ANO-DE-CONCLUSAO') or ''
        nome_agencia                             = texto.normaliza(graduacao.get('NOME-AGENCIA') or '')
  
        try:
          cursor.execute('INSERT INTO tab_3_formacao_academica_titulacao (docente, formacao_academica_titulacao, titulo_trabalho_conclusao_curso, nome_completo_orientador, nome_instituicao, curso, ano_de_inicio, ano_de_conclusao, nome_agencia, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, titulacao, titulo_do_trabalho_de_conclusao_de_curso, nome_do_orientador, nome_instituicao, nome_curso, ano_de_inicio, ano_de_conclusao, nome_agencia, identificacao))
          conexao.conn.commit()
          print('Formacao academica {0} inserida com sucesso!'.format(titulacao))
        except Exception as e:
          print('ERRO: Ao salvar a formacao academica {0}: '.format(titulacao))
          print(e)

      mestrado = formacao_academica_titulacao.find('MESTRADO')

      if mestrado != None:
        titulacao                    = 'MESTRADO'
        titulo_da_dissertacao_tese   = texto.normaliza(mestrado.get('TITULO-DA-DISSERTACAO-TESE') or '')
        nome_do_orientador           = texto.normaliza(mestrado.get('NOME-COMPLETO-DO-ORIENTADOR') or '')
        nome_instituicao             = texto.normaliza(mestrado.get('NOME-INSTITUICAO') or '')
        nome_curso                   = texto.normaliza(mestrado.get('NOME-CURSO') or '')
        ano_de_inicio                = mestrado.get('ANO-DE-INICIO') or ''
        ano_de_conclusao             = mestrado.get('ANO-DE-CONCLUSAO') or ''
        nome_agencia                 = texto.normaliza(mestrado.get('NOME-AGENCIA') or '')
  
        palavras_chave = mestrado.find('PALAVRAS-CHAVE')

        if palavras_chave != None:
          palavra_chave_1 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-1') or '')
          palavra_chave_2 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-2') or '')
          palavra_chave_3 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-3') or '')
          palavra_chave_4 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-4') or '')
          palavra_chave_5 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-5') or '')
          palavra_chave_6 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-6') or '')

        areas_do_conhecimento = mestrado.find('AREAS-DO-CONHECIMENTO')

        if areas_do_conhecimento != None:
          areas_do_conhecimento_1 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-1')

          if areas_do_conhecimento_1 != None:
            nome_grande_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_1     = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_1            = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_2 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-2')

          if areas_do_conhecimento_2 != None:
            nome_grande_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_2     = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_2            = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_3 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-3')

          if areas_do_conhecimento_3 != None:
            nome_grande_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_3     = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_3            = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-ESPECIALIDADE') or '')

        setores_de_atividade = mestrado.find('SETORES-DE-ATIVIDADE')

        if setores_de_atividade != None:
          setor_de_atividade_1 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-1') or '')
          setor_de_atividade_2 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-2') or '')
          setor_de_atividade_3 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-3') or '')

        try:
          cursor.execute('INSERT INTO tab_3_formacao_academica_titulacao (docente, formacao_academica_titulacao, titulo_dissertacao_ou_tese, nome_completo_orientador, nome_instituicao, curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_conhecimento1, nome_grande_area_conhecimento2, nome_grande_area_conhecimento3, nome_area_conhecimento1, nome_area_conhecimento2, nome_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_especialidade1, nome_especialidade2, nome_especialidade3, setor_de_atividade1, setor_de_atividade2, setor_de_atividade3, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, titulacao, titulo_da_dissertacao_tese, nome_do_orientador, nome_instituicao, nome_curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
          conexao.conn.commit()
          print('Formacao academica {0} inserida com sucesso!'.format(titulacao))
        except Exception as e:
          print('ERRO: Ao salvar a formacao academica {0}: '.format(titulacao))
          print(e)

      doutorado = formacao_academica_titulacao.find('DOUTORADO')

      if doutorado != None:
        titulacao                    = 'DOUTORADO'
        titulo_da_dissertacao_tese   = texto.normaliza(doutorado.get('TITULO-DA-DISSERTACAO-TESE') or '')
        nome_do_orientador           = texto.normaliza(doutorado.get('NOME-COMPLETO-DO-ORIENTADOR') or '')
        nome_instituicao             = texto.normaliza(doutorado.get('NOME-INSTITUICAO') or '')
        nome_curso                   = texto.normaliza(doutorado.get('NOME-CURSO') or '')
        ano_de_inicio                = doutorado.get('ANO-DE-INICIO') or ''
        ano_de_conclusao             = doutorado.get('ANO-DE-CONCLUSAO') or ''
        nome_agencia                 = texto.normaliza(doutorado.get('NOME-AGENCIA') or '')
  
        palavras_chave = doutorado.find('PALAVRAS-CHAVE')

        palavra_chave_1 = ''
        palavra_chave_2 = ''
        palavra_chave_3 = ''
        palavra_chave_4 = ''
        palavra_chave_5 = ''
        palavra_chave_6 = ''

        if palavras_chave != None:
          palavra_chave_1 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-1') or '')
          palavra_chave_2 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-2') or '')
          palavra_chave_3 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-3') or '')
          palavra_chave_4 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-4') or '')
          palavra_chave_5 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-5') or '')
          palavra_chave_6 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-6') or '')

        areas_do_conhecimento = doutorado.find('AREAS-DO-CONHECIMENTO')

        nome_grande_area_do_conhecimento_1 = ''
        nome_da_area_do_conhecimento_1     = ''
        nome_da_sub_area_do_conhecimento_1 = ''
        nome_da_especialidade_1            = ''
        nome_grande_area_do_conhecimento_2 = ''
        nome_da_area_do_conhecimento_2     = ''
        nome_da_sub_area_do_conhecimento_2 = ''
        nome_da_especialidade_2            = ''
        nome_grande_area_do_conhecimento_3 = ''
        nome_da_area_do_conhecimento_3     = ''
        nome_da_sub_area_do_conhecimento_3 = ''
        nome_da_especialidade_3            = ''

        if areas_do_conhecimento != None:
          areas_do_conhecimento_1 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-1')

          if areas_do_conhecimento_1 != None:
            nome_grande_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_1     = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_1            = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_2 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-2')

          if areas_do_conhecimento_2 != None:
            nome_grande_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_2     = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_2            = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_3 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-3')

          if areas_do_conhecimento_3 != None:
            nome_grande_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_3     = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_3            = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-ESPECIALIDADE') or '')

        setores_de_atividade = doutorado.find('SETORES-DE-ATIVIDADE')

        setor_de_atividade_1 = ''
        setor_de_atividade_2 = ''
        setor_de_atividade_3 = ''

        if setores_de_atividade != None:
          setor_de_atividade_1 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-1') or '')
          setor_de_atividade_2 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-2') or '')
          setor_de_atividade_3 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-3') or '')

        try:
          cursor.execute('INSERT INTO tab_3_formacao_academica_titulacao (docente, formacao_academica_titulacao, titulo_dissertacao_ou_tese, nome_completo_orientador, nome_instituicao, curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_conhecimento1, nome_grande_area_conhecimento2, nome_grande_area_conhecimento3, nome_area_conhecimento1, nome_area_conhecimento2, nome_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_especialidade1, nome_especialidade2, nome_especialidade3, setor_de_atividade1, setor_de_atividade2, setor_de_atividade3, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, titulacao, titulo_da_dissertacao_tese, nome_do_orientador, nome_instituicao, nome_curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
          conexao.conn.commit()
          print('Formacao academica {0} inserida com sucesso!'.format(titulacao))
        except Exception as e:
          print('ERRO: Ao salvar a formacao academica {0}: '.format(titulacao))
          print(e)

      pos_doutorado = formacao_academica_titulacao.find('POS-DOUTORADO')

      if pos_doutorado != None:
        titulacao                    = 'POS-DOUTORADO'
        titulo_da_dissertacao_tese   = texto.normaliza(pos_doutorado.get('TITULO-DA-DISSERTACAO-TESE') or '')
        nome_do_orientador           = texto.normaliza(pos_doutorado.get('NOME-COMPLETO-DO-ORIENTADOR') or '')
        nome_instituicao             = texto.normaliza(pos_doutorado.get('NOME-INSTITUICAO') or '')
        nome_curso                   = texto.normaliza(pos_doutorado.get('NOME-CURSO') or '')
        ano_de_inicio                = pos_doutorado.get('ANO-DE-INICIO') or ''
        ano_de_conclusao             = pos_doutorado.get('ANO-DE-CONCLUSAO') or ''
        nome_agencia                 = texto.normaliza(pos_doutorado.get('NOME-AGENCIA') or '')
  
        palavras_chave = pos_doutorado.find('PALAVRAS-CHAVE')

        if palavras_chave != None:
          palavra_chave_1 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-1') or '')
          palavra_chave_2 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-2') or '')
          palavra_chave_3 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-3') or '')
          palavra_chave_4 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-4') or '')
          palavra_chave_5 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-5') or '')
          palavra_chave_6 = texto.normaliza(palavras_chave.get('PALAVRA-CHAVE-6') or '')

        areas_do_conhecimento = pos_doutorado.find('AREAS-DO-CONHECIMENTO')

        if areas_do_conhecimento != None:
          areas_do_conhecimento_1 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-1')

          if areas_do_conhecimento_1 != None:
            nome_grande_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_1     = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_1 = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_1            = texto.normaliza(areas_do_conhecimento_1.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_2 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-2')

          if areas_do_conhecimento_2 != None:
            nome_grande_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_2     = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_2 = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_2            = texto.normaliza(areas_do_conhecimento_2.get('NOME-DA-ESPECIALIDADE') or '')

          areas_do_conhecimento_3 = areas_do_conhecimento.find('AREA-DO-CONHECIMENTO-3')

          if areas_do_conhecimento_3 != None:
            nome_grande_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-GRANDE-AREA-DO-CONHECIMENTO') or '')
            nome_da_area_do_conhecimento_3     = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-AREA-DO-CONHECIMENTO') or '')
            nome_da_sub_area_do_conhecimento_3 = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-SUB-AREA-DO-CONHECIMENTO') or '')
            nome_da_especialidade_3            = texto.normaliza(areas_do_conhecimento_3.get('NOME-DA-ESPECIALIDADE') or '')

        setores_de_atividade = pos_doutorado.find('SETORES-DE-ATIVIDADE')

        if setores_de_atividade != None:
          setor_de_atividade_1 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-1') or '')
          setor_de_atividade_2 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-2') or '')
          setor_de_atividade_3 = texto.normaliza(palavras_chave.get('SETOR-DE-ATIVIDADE-3') or '')

        try:
          cursor.execute('INSERT INTO tab_3_formacao_academica_titulacao (docente, formacao_academica_titulacao, titulo_dissertacao_ou_tese, nome_completo_orientador, nome_instituicao, curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_conhecimento1, nome_grande_area_conhecimento2, nome_grande_area_conhecimento3, nome_area_conhecimento1, nome_area_conhecimento2, nome_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_especialidade1, nome_especialidade2, nome_especialidade3, setor_de_atividade1, setor_de_atividade2, setor_de_atividade3, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, titulacao, titulo_da_dissertacao_tese, nome_do_orientador, nome_instituicao, nome_curso, ano_de_inicio, ano_de_conclusao, nome_agencia, palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
          conexao.conn.commit()
          print('Formacao academica {0} inserida com sucesso!'.format(titulacao))
        except Exception as e:
          print('ERRO: Ao salvar a formacao academica {0}: '.format(titulacao))
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()