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

      trabalhos_tecnicos = producao_tecnica.findall('TRABALHO-TECNICO')

      for trabalho_tecnico in trabalhos_tecnicos:

        dados_basicos_do_trabalho_tecnico = trabalho_tecnico.find('DADOS-BASICOS-DO-TRABALHO-TECNICO')
        detalhamento_do_trabalho_tecnico  = trabalho_tecnico.find('DETALHAMENTO-DO-TRABALHO-TECNICO')
        palavras_chave                    = trabalho_tecnico.find('PALAVRAS-CHAVE')
        autores                           = trabalho_tecnico.findall('AUTORES')
        areas_do_conhecimento             = trabalho_tecnico.find('AREAS-DO-CONHECIMENTO')
        setores_de_atividade              = trabalho_tecnico.find('SETORES-DE-ATIVIDADE')

        if dados_basicos_do_trabalho_tecnico != None:

          natureza                   = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('NATUREZA') or '')
          titulo_do_trabalho_tecnico = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('TITULO-DO-TRABALHO-TECNICO') or '')
          ano                        = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('ANO') or '')
          pais                       = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('PAIS') or '')
          idioma                     = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('IDIOMA') or '')
          meio_de_divulgacao         = texto.normaliza(dados_basicos_do_trabalho_tecnico.get('MEIO-DE-DIVULGACAO') or '')

        if detalhamento_do_trabalho_tecnico != None:

          finalidade               = texto.normaliza(detalhamento_do_trabalho_tecnico.get('FINALIDADE') or '')
          instituicao_financiadora = texto.normaliza(detalhamento_do_trabalho_tecnico.get('INSTITUICAO-FINANCIADORA') or '')
          cidade_do_trabalho       = texto.normaliza(detalhamento_do_trabalho_tecnico.get('CIDADE-DO-TRABALHO') or '')

        nomes_autores = []
        autorias      = []

        for autor in autores:
          
          nome_completo_do_autor = texto.normaliza(autor.get('NOME-COMPLETO-DO-AUTOR') or '')
          ordem_de_autoria       = texto.normaliza(autor.get('ORDEM-DE-AUTORIA') or '')

          nomes_autores.append(nome_completo_do_autor)
          autorias.append(ordem_de_autoria)

        # Obs.: Há docentes com um número elevado de autorias, porém o banco foi feito para suportar apenas três
        campo_autores  = [''] * 5
        campo_autorias = [''] * 5

        for index, nome_autor in enumerate(nomes_autores[:5]):
          campo_autores[index] = nome_autor

        for index, autoria in enumerate(autorias[:5]):
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
          cursor.execute("""INSERT INTO tab_21_dados_basicos_trabalho_tecnico 
                        (docente, natureza, titulo_do_trabalho_tecnico, ano, pais, idioma, meio_de_divulgacao, finalidade, instituicao_financiadora, nome_ccompleto_autor1, nome_ccompleto_autor2, nome_ccompleto_autor3, nome_ccompleto_autor4, nome_ccompleto_autor5, ordem_da_autoria1, ordem_da_autoria2, ordem_da_autoria3, ordem_da_autoria4, ordem_da_autoria5, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_do_conhecimento1, nome_grande_area_do_conhecimento2, nome_grande_area_do_conhecimento3, nome_da_area_conhecimento1, nome_da_area_conhecimento2, nome_da_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_da_especialidade1, nome_da_especialidade2, nome_da_especialidade3, setor_da_atividade1, setor_da_atividade2, setor_da_atividade3, id_1dados_gerais) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                        (nome_do_docente, natureza, titulo_do_trabalho_tecnico, ano, pais, idioma, meio_de_divulgacao, finalidade, instituicao_financiadora, campo_autores[0], campo_autores[1], campo_autores[2], campo_autores[3], campo_autores[4], campo_autorias[0], campo_autorias[1], campo_autorias[2], campo_autorias[3], campo_autorias[4], palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
          conexao.conn.commit()
          print('Trabalho Tecnico inserida com sucesso!')
        except Exception as e:
          print('ERRO: Ao salvar o Trabalho Tecnico')
          print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
