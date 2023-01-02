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

        atividades_de_pesquisa_e_desenvolvimento = atuacao_profissional.find('ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO')

        if atividades_de_pesquisa_e_desenvolvimento != None:

          pesquisa_e_desenvolvimentos = atividades_de_pesquisa_e_desenvolvimento.findall('PESQUISA-E-DESENVOLVIMENTO')

          for  pesquisa_e_desenvolvimento in pesquisa_e_desenvolvimentos:

            ano_inicio       = texto.normaliza(pesquisa_e_desenvolvimento.get('ANO-INICIO') or '')
            ano_fim          = texto.normaliza(pesquisa_e_desenvolvimento.get('ANO-FIM') or '')
            nome_orgao       = texto.normaliza(pesquisa_e_desenvolvimento.get('NOME-ORGAO') or '')
            nome_unidade     = texto.normaliza(pesquisa_e_desenvolvimento.get('NOME-UNIDADE') or '')

            linha_de_pesquisa = pesquisa_e_desenvolvimento.find('LINHA-DE-PESQUISA')

            titulo_da_linha_de_pesquisa  = ''
            flag_linha_de_pesquisa_ativa = ''
            objetivos_linha_de_pesquisa  = ''

            if linha_de_pesquisa != None:
              titulo_da_linha_de_pesquisa  = texto.normaliza(linha_de_pesquisa.get('TITULO-DA-LINHA-DE-PESQUISA') or '')
              flag_linha_de_pesquisa_ativa = texto.normaliza(linha_de_pesquisa.get('FLAG-LINHA-DE-PESQUISA-ATIVA') or '')
              objetivos_linha_de_pesquisa  = texto.normaliza(linha_de_pesquisa.get('OBJETIVOS-LINHA-DE-PESQUISA') or '')

            palavras_chave = pesquisa_e_desenvolvimento.find('PALAVRAS-CHAVE')

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

            areas_do_conhecimento = pesquisa_e_desenvolvimento.find('AREAS-DO-CONHECIMENTO')

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

            setores_de_atividade = pesquisa_e_desenvolvimento.find('SETORES-DE-ATIVIDADE')

            setor_de_atividade_1 = ''
            setor_de_atividade_2 = ''
            setor_de_atividade_3 = ''

            if setores_de_atividade != None:
              setor_de_atividade_1 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-1') or '')
              setor_de_atividade_2 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-2') or '')
              setor_de_atividade_3 = texto.normaliza(setores_de_atividade.get('SETOR-DE-ATIVIDADE-3') or '')

            try:
              cursor.execute('INSERT INTO tab_6_atividade_pesquisa_desenvolvimento (docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, titulo_linha_pesquisa, flag_linha_pesquisa_ativa, objetivos_linha_pesquisa, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_conhecimento1, nome_grande_area_conhecimento2, nome_grande_area_conhecimento3, nome_area_conhecimento1, nome_area_conhecimento2, nome_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_da_especialidade1, nome_da_especialidade2, nome_da_especialidade3, setor_atividade1, setor_atividade2, setor_atividade3, id_1dados_gerais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nome_do_docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, titulo_da_linha_de_pesquisa, flag_linha_de_pesquisa_ativa, objetivos_linha_de_pesquisa, palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
              conexao.conn.commit()
              print('Atividade Pesquisa Desenvolvimento inserida com sucesso!')
            except Exception as e:
              print('ERRO: Ao salvar a Atividade Pesquisa Desenvolvimento: ')
              print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
