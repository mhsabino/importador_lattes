from enum import auto
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

  dados_gerais 	        = root.find('DADOS-GERAIS')
  dados_complementares  = root.find('DADOS-COMPLEMENTARES')
  nome_do_docente       = texto.normaliza(dados_gerais.get('NOME-COMPLETO'))
  
  print('*'*20)
  print('nome_do_docente', nome_do_docente)

  cursor.execute('SELECT id_1dados_gerais FROM tab_1_dados_gerais WHERE nome_completo = %s', (nome_do_docente,))

  identificacao = 0
  row = cursor.fetchone()
  conexao.conn.commit()

  try:
    identificacao = row[0]
    print(identificacao)

    if dados_complementares != None:

      participacao_em_banca_trabalhos_conclusao = dados_complementares.find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')
      
      if participacao_em_banca_trabalhos_conclusao != None:

        participacao_em_banca_de_exames_qualificacoes = participacao_em_banca_trabalhos_conclusao.findall('PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO')

        for participacao_em_banca_de_qualificacao in participacao_em_banca_de_exames_qualificacoes:

          dados_basicos         = participacao_em_banca_de_qualificacao.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO')
          detalhamento          = participacao_em_banca_de_qualificacao.find('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO')
          palavras_chave        = participacao_em_banca_de_qualificacao.find('PALAVRAS-CHAVE')
          participantes         = participacao_em_banca_de_qualificacao.findall('PARTICIPANTE-BANCA')
          areas_do_conhecimento = participacao_em_banca_de_qualificacao.find('AREAS-DO-CONHECIMENTO')
          setores_de_atividade  = participacao_em_banca_de_qualificacao.find('SETORES-DE-ATIVIDADE')

          if dados_basicos != None:

            natureza           = texto.normaliza(dados_basicos.get('NATUREZA') or '')
            tipo               = texto.normaliza(dados_basicos.get('TIPO') or '')
            titulo             = texto.normaliza(dados_basicos.get('TITULO') or '')
            ano                = texto.normaliza(dados_basicos.get('ANO') or '')
            pais               = texto.normaliza(dados_basicos.get('PAIS') or '')
            idioma             = texto.normaliza(dados_basicos.get('IDIOMA') or '')

          if detalhamento != None:

            nome_do_candidato            = texto.normaliza(detalhamento.get('NOME-DO-CANDIDATO') or '')
            nome_instituicao             = texto.normaliza(detalhamento.get('NOME-INSTITUICAO') or '')
            nome_orgao                   = texto.normaliza(detalhamento.get('NOME-ORGAO') or '')
            nome_curso                   = texto.normaliza(detalhamento.get('NOME-CURSO') or '')

          nomes_participantes = []
          ordem_participantes = []

          for participante in participantes:
            
            nome_completo_do_participante = texto.normaliza(participante.get('NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA') or '')
            ordem_do_participante         = texto.normaliza(participante.get('ORDEM-PARTICIPANTE') or '')

            nomes_participantes.append(nome_completo_do_participante)
            ordem_participantes.append(ordem_do_participante)

          # Obs.: Há docentes com um número elevado de ordens, porém o banco foi feito para suportar apenas três
          campo_participantes = [''] * 50
          campo_participantes = [''] * 50

          for index, nome_participante in enumerate(nomes_participantes):
            campo_participantes[index] = nome_participante

          for index, ordem in enumerate(ordem_participantes):
            campo_participantes[index] = ordem

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

          setor_de_atividade_1 = ''
          setor_de_atividade_2 = ''
          setor_de_atividade_3 = ''

          if setores_de_atividade != None:
            setor_de_atividade_1 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-1') or '')
            setor_de_atividade_2 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-2') or '')
            setor_de_atividade_3 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-3') or '')

          try:
            cursor.execute("""INSERT INTO tab_29_participaoes_em_bancas 
                          (docente, natureza, tipo, ano, pais, idioma, nome_do_candidato, nome_instituicao, nome_orgao, nome_curso, nome_completo_do_participante_da_banca1, nome_completo_do_participante_da_banca2, nome_completo_do_participante_da_banca3, nome_completo_do_participante_da_banca4, nome_completo_do_participante_da_banca5, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_do_conhecimento1, nome_grande_area_do_conhecimento2, nome_grande_area_do_conhecimento3, nome_da_area_conhecimento1, nome_da_area_conhecimento2, nome_da_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_da_especialidade1, nome_da_especialidade2, nome_da_especialidade3, setor_da_atividade1, setor_da_atividade2, setor_da_atividade3) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                          (nome_do_docente, natureza, tipo, ano, pais, idioma, nome_do_candidato, nome_instituicao, nome_orgao, nome_curso, campo_participantes[0], campo_participantes[1], campo_participantes[2], campo_participantes[3], campo_participantes[4], palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_3, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3))
            conexao.conn.commit()
            print('Participacao exame qualificacao inserida com sucesso!')
          except Exception as e:
            print('ERRO: Ao salvar o Participacao exame qualificacao')
            print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
