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

  dados_gerais 	   = root.find('DADOS-GERAIS')
  producao_tecnica = root.find('PRODUCAO-TECNICA')
  nome_do_docente  = texto.normaliza(dados_gerais.get('NOME-COMPLETO'))
  
  print('*'*20)
  print('nome_do_docente', nome_do_docente)

  cursor.execute('SELECT id_1dados_gerais FROM tab_1_dados_gerais WHERE nome_completo = %s', (nome_do_docente,))

  identificacao = 0
  row = cursor.fetchone()
  conexao.conn.commit()

  try:
    identificacao = row[0]
    print(identificacao)

    if producao_tecnica != None:

      demais_tipos_de_producao_tecnica_grupo = producao_tecnica.find('DEMAIS-TIPOS-DE-PRODUCAO-TECNICA')
      
      if demais_tipos_de_producao_tecnica_grupo != None:

        relatorio_de_pesquisas = demais_tipos_de_producao_tecnica_grupo.findall('RELATORIO-DE-PESQUISA')

        for relatorio_de_pesquisa in relatorio_de_pesquisas:

          dados_basicos         = relatorio_de_pesquisa.find('DADOS-BASICOS-DO-RELATORIO-DE-PESQUISA')
          detalhamento          = relatorio_de_pesquisa.find('DETALHAMENTO-DO-RELATORIO-DE-PESQUISA')
          palavras_chave        = relatorio_de_pesquisa.find('PALAVRAS-CHAVE')
          autores               = relatorio_de_pesquisa.findall('AUTORES')
          areas_do_conhecimento = relatorio_de_pesquisa.find('AREAS-DO-CONHECIMENTO')
          setores_de_atividade  = relatorio_de_pesquisa.find('SETORES-DE-ATIVIDADE')

          if dados_basicos != None:

            titulo             = texto.normaliza(dados_basicos.get('TITULO') or '')
            ano                = texto.normaliza(dados_basicos.get('ANO') or '')
            pais               = texto.normaliza(dados_basicos.get('PAIS') or '')
            idioma             = texto.normaliza(dados_basicos.get('IDIOMA') or '')
            meio_de_divulgacao = texto.normaliza(dados_basicos.get('MEIO-DE-DIVULGACAO') or '')

          if detalhamento != None:

            nome_do_projeto          = texto.normaliza(detalhamento.get('NOME-DO-PROJETO') or '')
            numero_de_paginas        = texto.normaliza(detalhamento.get('NUMERO-DE-PAGINAS') or '')
            disponibilidade          = texto.normaliza(detalhamento.get('DISPONIBILIDADE') or '')
            instituicao_financiadora = texto.normaliza(detalhamento.get('INSTITUICAO-FINANCIADORA') or '')

          nomes_autores = []
          autorias      = []

          for autor in autores:
            
            nome_completo_do_autor = texto.normaliza(autor.get('NOME-COMPLETO-DO-AUTOR') or '')
            ordem_de_autoria       = texto.normaliza(autor.get('ORDEM-DE-AUTORIA') or '')

            nomes_autores.append(nome_completo_do_autor)
            autorias.append(ordem_de_autoria)

          # Obs.: Há docentes com um número elevado de autorias, porém o banco foi feito para suportar apenas três
          campo_autores  = [''] * 50
          campo_autorias = [''] * 50

          for index, nome_autor in enumerate(nomes_autores):
            campo_autores[index] = nome_autor

          for index, autoria in enumerate(autorias):
            campo_autorias[index] = autoria

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
            cursor.execute("""INSERT INTO tab_27_relatoria_pesquisa 
                          (docente, titulo, ano, pais, meio_de_divulgacao, nome_do_projeto, numero_paginas, disponibilidade, instituicao_financiadora1, nome_completo_autor1, nome_completo_autor2, nome_completo_autor3, nome_completo_autor4, nome_completo_autor5, nome_completo_autor6, nome_completo_autor7, nome_completo_autor8, nome_completo_autor9, nome_completo_autor10, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_do_conhecimento1, nome_grande_area_do_conhecimento2, nome_grande_area_do_conhecimento3, nome_da_area_conhecimento1, nome_da_area_conhecimento2, nome_da_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_da_especialidade1, nome_da_especialidade2, nome_da_especialidade3, setor_da_atividade1, setor_da_atividade2, setor_da_atividade3) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                          (nome_do_docente, titulo, ano, pais, meio_de_divulgacao, nome_do_projeto, numero_de_paginas, disponibilidade, instituicao_financiadora, campo_autores[0], campo_autores[1], campo_autores[2], campo_autores[3], campo_autores[4], campo_autores[5], campo_autores[6], campo_autores[7], campo_autores[8], campo_autores[9], palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3))
            conexao.conn.commit()
            print('Relatorio de pesquisa inserido com sucesso!')
          except Exception as e:
            print('ERRO: Ao salvar o Relatorio de pesquisa')
            print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
