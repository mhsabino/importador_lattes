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

  dados_gerais 	         = root.find('DADOS-GERAIS')
  producao_bibliografica = root.find('PRODUCAO-BIBLIOGRAFICA')
  nome_do_docente        = texto.normaliza(dados_gerais.get('NOME-COMPLETO'))
  
  print('*'*20)
  print('nome_do_docente', nome_do_docente)

  cursor.execute('SELECT id_1dados_gerais FROM tab_1_dados_gerais WHERE nome_completo = %s', (nome_do_docente,))

  identificacao = 0
  row = cursor.fetchone()
  conexao.conn.commit()

  try:
    identificacao = row[0]
    print(identificacao)

    if producao_bibliografica != None:
    
      textos_em_jornais_ou_revistas_grupo = producao_bibliografica.find('TEXTOS-EM-JORNAIS-OU-REVISTAS')

      if textos_em_jornais_ou_revistas_grupo != None:

        texto_em_jornal_ou_revistas = textos_em_jornais_ou_revistas_grupo.findall('TEXTO-EM-JORNAL-OU-REVISTA')

        for texto_em_jornal_ou_revista in texto_em_jornal_ou_revistas:

          dados_basicos_do_artigo = texto_em_jornal_ou_revista.find('DADOS-BASICOS-DO-TEXTO')
          detalhamento_do_artigo  = texto_em_jornal_ou_revista.find('DETALHAMENTO-DO-TEXTO')
          palavras_chave          = texto_em_jornal_ou_revista.find('PALAVRAS-CHAVE')
          autores                 = texto_em_jornal_ou_revista.findall('AUTORES')
          areas_do_conhecimento   = texto_em_jornal_ou_revista.find('AREAS-DO-CONHECIMENTO')
          setores_de_atividade    = texto_em_jornal_ou_revista.find('SETORES-DE-ATIVIDADE')

          if dados_basicos_do_artigo != None:

            natureza           = texto.normaliza(dados_basicos_do_artigo.get('NATUREZA') or '')
            titulo_do_texto    = texto.normaliza(dados_basicos_do_artigo.get('TITULO-DO-TEXTO') or '')
            ano_do_texto       = texto.normaliza(dados_basicos_do_artigo.get('ANO-DO-TEXTO') or '')
            pais               = texto.normaliza(dados_basicos_do_artigo.get('PAIS-DE-PUBLICACAO') or '')
            idioma             = texto.normaliza(dados_basicos_do_artigo.get('IDIOMA') or '')
            meio_de_divulgacao = texto.normaliza(dados_basicos_do_artigo.get('MEIO-DE-DIVULGACAO') or '')

          if detalhamento_do_artigo != None:

            titulo_do_jornal_ou_revista = texto.normaliza(detalhamento_do_artigo.get('TITULO-DO-JORNAL-OU-REVISTA') or '')
            volume                      = texto.normaliza(detalhamento_do_artigo.get('VOLUME') or '')
            pagina_inicial              = texto.normaliza(detalhamento_do_artigo.get('PAGINA-INICIAL') or '')
            pagina_final                = texto.normaliza(detalhamento_do_artigo.get('PAGINA-FINAL') or '')
            local_de_publicacao         = texto.normaliza(detalhamento_do_artigo.get('LOCAL-DE-PUBLICACAO') or '')

          nomes_autores = []

          for autor in autores:
            
            nome_completo_do_autor = texto.normaliza(autor.get('NOME-COMPLETO-DO-AUTOR') or '')

            nomes_autores.append(nome_completo_do_autor)

          campo_autores  = [''] * 3

          for index, nome_autor in enumerate(nomes_autores[:3]):
            campo_autores[index] = nome_autor

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
            cursor.execute("""INSERT INTO tab_18_textos_jornal_ou_revistas 
                          (docente, natureza, titulo_do_texto, ano_do_texto, pais_de_publicacao, idioma, meio_de_divulgacao, titulo_jornal_ou_revista, volume, pagina_inicial, pagina_final, local_de_publicacao, nome_ccompleto_autor1, nome_ccompleto_autor2, nome_ccompleto_autor3, palavra_chave1, palavra_chave2, palavra_chave3, palavra_chave4, palavra_chave5, palavra_chave6, nome_grande_area_do_conhecimento1, nome_grande_area_do_conhecimento2, nome_grande_area_do_conhecimento3, nome_da_area_conhecimento1, nome_da_area_conhecimento2, nome_da_area_conhecimento3, nome_sub_area_conhecimento1, nome_sub_area_conhecimento2, nome_sub_area_conhecimento3, nome_da_especialidade1, nome_da_especialidade2, nome_da_especialidade3, setor_da_atividade1, setor_da_atividade2, setor_da_atividade3, id_1dados_gerais) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                          (nome_do_docente, natureza, titulo_do_texto, ano_do_texto, pais, idioma, meio_de_divulgacao, titulo_do_jornal_ou_revista, volume, pagina_inicial, pagina_final, local_de_publicacao, campo_autores[0], campo_autores[1], campo_autores[2], palavra_chave_1, palavra_chave_2, palavra_chave_3, palavra_chave_4, palavra_chave_5, palavra_chave_6, nome_grande_area_do_conhecimento_1, nome_grande_area_do_conhecimento_2, nome_grande_area_do_conhecimento_3, nome_da_area_do_conhecimento_1, nome_da_area_do_conhecimento_2, nome_da_area_do_conhecimento_3, nome_da_sub_area_do_conhecimento_1, nome_da_sub_area_do_conhecimento_2, nome_da_sub_area_do_conhecimento_3, nome_da_especialidade_1, nome_da_especialidade_2, nome_da_especialidade_3, setor_de_atividade_1, setor_de_atividade_2, setor_de_atividade_3, identificacao))
            conexao.conn.commit()
            print('Texto em Jornal ou Revista inserido com sucesso!')
          except Exception as e:
            print('ERRO: Ao salvar o Texto em Jornal ou Revista')
            print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
