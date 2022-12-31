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

        atividades_de_participacao_em_projeto = atuacao_profissional.find('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')

        if atividades_de_participacao_em_projeto != None:

          participacao_em_projetos = atividades_de_participacao_em_projeto.findall('PARTICIPACAO-EM-PROJETO')

          for participacao_em_projeto in participacao_em_projetos:

            ano_inicio   = texto.normaliza(participacao_em_projeto.get('ANO-INICIO') or '')
            ano_fim      = texto.normaliza(participacao_em_projeto.get('ANO-FIM') or '')
            nome_orgao   = texto.normaliza(participacao_em_projeto.get('NOME-ORGAO') or '')
            nome_unidade = texto.normaliza(participacao_em_projeto.get('NOME-UNIDADE') or '')

            projeto_de_pesquisa = participacao_em_projeto.find('PROJETO-DE-PESQUISA')

            if projeto_de_pesquisa != None:

              nome_do_projeto           = texto.normaliza(projeto_de_pesquisa.get('NOME-DO-PROJETO') or '')
              situacao                  = texto.normaliza(projeto_de_pesquisa.get('SITUACAO') or '')
              natureza                  = texto.normaliza(projeto_de_pesquisa.get('NATUREZA') or '')
              numero_graduacao          = texto.normaliza(projeto_de_pesquisa.get('NUMERO-GRADUACAO') or '')
              numero_especializacao     = texto.normaliza(projeto_de_pesquisa.get('NUMERO-ESPECIALIZACAO') or '')
              numero_mestrado_academico = texto.normaliza(projeto_de_pesquisa.get('NUMERO-MESTRADO-ACADEMICO') or '')
              numero_mestrado_prof      = texto.normaliza(projeto_de_pesquisa.get('NUMERO-MESTRADO-PROF') or '')
              numero_doutorado          = texto.normaliza(projeto_de_pesquisa.get('NUMERO-DOUTORADO') or '')
              descricao_do_projeto      = texto.normaliza(projeto_de_pesquisa.get('DESCRICAO-DO-PROJETO') or '')

              equipe_do_projeto        = projeto_de_pesquisa.find('EQUIPE-DO-PROJETO')
              financiadores_do_projeto = projeto_de_pesquisa.find('FINANCIADORES-DO-PROJETO')

              campo_nomes         = [''] * 50
              campo_ordens        = [''] * 50
              campo_flags         = [''] * 50
              campo_instituicoes  = [''] * 50
              campo_naturezas     = [''] * 50

              if equipe_do_projeto != None:

                integrantes_dos_projetos = equipe_do_projeto.findall('INTEGRANTES-DO-PROJETO')

                nomes_completos       = []
                ordem_de_integracaoes = []
                flags_responsaveis    = []

                for integrante_do_projeto in integrantes_dos_projetos:

                  nome_completo        = texto.normaliza(integrante_do_projeto.get('NOME-COMPLETO') or '')
                  ordem_de_integracao  = texto.normaliza(integrante_do_projeto.get('ORDEM-DE-INTEGRACAO') or '')
                  flag_responsavel     = texto.normaliza(integrante_do_projeto.get('FLAG-RESPONSAVEL') or '')

                  nomes_completos.append(nome_completo)
                  ordem_de_integracaoes.append(ordem_de_integracao)
                  flags_responsaveis.append(flag_responsavel)

                for index, nome_completo in enumerate(nomes_completos):
                  campo_nomes[index] = nome_completo

                for index, ordem in enumerate(ordem_de_integracaoes):
                  campo_ordens[index] = ordem

                for index, flag in enumerate(flags_responsaveis):
                  campo_flags[index] = flag

              if financiadores_do_projeto != None:

                financiador_dos_projetos = financiadores_do_projeto.findall('FINANCIADOR-DO-PROJETO')

                naturezas    = []
                instituicoes = []

                for financiador_do_projeto in financiador_dos_projetos:

                  nome_instituicao = texto.normaliza(financiador_do_projeto.get('NOME-INSTITUICAO') or '')
                  natureza         = texto.normaliza(financiador_do_projeto.get('NATUREZA') or '')

                  instituicoes.append(nome_instituicao)
                  naturezas.append(natureza)

                for index, instituicao in enumerate(instituicoes):
                  campo_instituicoes[index] = instituicao

                for index, natureza in enumerate(naturezas):
                  campo_naturezas[index] = natureza

              try:
                cursor.execute("""INSERT INTO tab_12_participacao_projeto 
                                  (docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, nome_do_projeto, situacao, natureza, numero_graduacao, numero_especializacao, numero_mestrado_academico, numero_mestrado_profissional, numero_doutorado, descricao_do_projeto, nome_completo1, nome_completo2, nome_completo3, nome_completo4, nome_completo5, nome_completo6, nome_completo7, nome_completo8, nome_completo9, nome_completo10, nome_completo11, nome_completo12, flag_responsavel1, flag_responsavel2, flag_responsavel3, flag_responsavel4, flag_responsavel5, nome_instituicao1, nome_instituicao2, nome_instituicao3, natureza1, natureza2, natureza3, id_1dados_gerais) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                                  (nome_do_docente, ano_inicio, ano_fim, nome_orgao, nome_unidade, nome_do_projeto, situacao, natureza, numero_graduacao, numero_especializacao, numero_mestrado_academico, numero_mestrado_prof, numero_doutorado, descricao_do_projeto, campo_nomes[0], campo_nomes[1], campo_nomes[2], campo_nomes[3], campo_nomes[4], campo_nomes[5], campo_nomes[6], campo_nomes[7], campo_nomes[8], campo_nomes[9], campo_nomes[10], campo_nomes[11], campo_flags[0], campo_flags[1], campo_flags[2], campo_flags[3], campo_flags[4], campo_instituicoes[0], campo_instituicoes[1], campo_instituicoes[2], campo_naturezas[0], campo_naturezas[1], campo_naturezas[2], identificacao))
                conexao.conn.commit()
                print('Participacao Projeto inserida com sucesso!')
              except Exception as e:
                print('ERRO: Ao salvar a Participacao Projeto {0}: ')
                print(e)

  except TypeError as e:
    print(identificacao)
    print(e)
    print("O docente '{0}' não existe no banco de dados.".format(nome_do_docente))
    continue

conexao.conn.close()
