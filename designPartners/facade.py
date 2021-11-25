#! virtualenv/bin/env python
from math import nan
from accessWPensar.dataFrame import *
from manipulationCSV.dataFrame import *
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode

class InclusionManager(object):
    def __init__(self):
        print("Iniciando processo de inclusão dos alunos na plataforma WPensar \n")
        self.getDataframeStatus()
        self.getTables()

    def getDataframeStatus(self):
        import os
        print('Carregando as informações das inclusões já realizadas...')
        try:
            fileNameDataframe = os.path.join(os.path.dirname(__file__),'dataframe.json')
            self.dataframeStatus = pd.read_csv(fileNameDataframe)
            print('Arquivo carregado com sucesso\n\n')
        except:
            print('Não existem informações\n\n')
            self.dataframeStatus = None

    def getTables(self):
        self.getTableCSV()
        self.getTableWPensar()

    def getTableCSV(self):
        self.dataBaseClickSign = DataBaseClickSign('Relatório - matrículas internas - TESTE.csv')
        # self.dataBaseClickSign = DataBaseClickSign('Relatório - matrículas internas.csv')
        
        # self.dataBaseClickSign = DataBaseClickSign('Relatório -matrículas internas excepcionais.csv')
        # self.dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas.csv')
        # self.dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas - excepcionais.csv')
        self.ClickSign = self.dataBaseClickSign.dataframeTreated

    def getTableWPensar(self):
        self.WPensar = DataBaseWPensar()

    def calculateSimilarity(self, text1, text2):
        import jellyfish as jf
        
        return jf.levenshtein_distance(''.join(text1.split()), ''.join(text2.split()))

    def stringComparation(self, text1, text2):
        try:
            similarity = self.calculateSimilarity(unidecode(text1.upper()), unidecode(text2.upper()))

            if similarity == 0:
                if unidecode(''.join(text1.upper().split())) == unidecode(''.join(text2.upper().split())):
                    # print(similarity)
                    return True   # The strings are the same
                else:
                    return False  # The strings aren't the same
            else:
                return False
        except:
            return False

    def searchInWPensar(self, text1, target = 'alunos'):
        if target =='alunos':
            matricula = False
            for row in self.WPensar.alunos[['nome', 'matricula']].to_numpy():
                if self.stringComparation(text1, row[0]):
                    matricula = row[1]
            if type(matricula) is not bool:
                # print(f"{matricula}: {text1}")
                return matricula
            else:
                return 0
        elif target == 'responsaveis':
            codResponsavel = False
            for row in self.WPensar.responsaveis[['nome', 'codigo']].to_numpy():
                if self.stringComparation(text1, row[0]):
                    codResponsavel = row[1]
            if type(codResponsavel) is not bool:
                return codResponsavel
            else:
                return 0
        else:
            return 0

    def doInclude(self, data = None, target = 'alunos'):
        """
        This function returns pk number after consult or inclusion data at WPensar
        """
        data = self.ClickSign if data is None else data
        
        if data['status'] == "Finalizado" and not data['teste']:
            # Busca a informação de novo aluno na tabela da clickSign
            if target == 'alunos':
                isNewData = data['novo_aluno']
                isExistWPensar = data['matriculaWPensar']
            elif target == 'responsaveis':
                isNewData = data['novo_responsavel']
                isExistWPensar = data['codigoResponsavel']
            else:
                return None
            # Verifica nos dados importados na WPensar
            
            # print("\nIniciando inclusão de alunos...")
            if (isNewData and isExistWPensar != 0): #True and True
                """
                Apesar de ser considerada uma nova entrada,
                o dado já existe na plataforma
                retornaremos seu id
                """
                
                # PRECISO INCLUIR O SEND DATA
                return "Novo dado já existe na WPensar - Dados atualizados."
            elif (isNewData and isExistWPensar == 0): #True and False
                '''
                A informação é nova e ainda não foi inserido na plataforma
                Após a inclusão, retornaremos seu id
                '''
                # self.sendDataToWPensar(target=target, data = data)
                   
                return "Novos dados incluídos na plataforma."
            elif (not isNewData and isExistWPensar != 0): #False and True
                """
                A informação já existe na plataforma
                retornaremos seu id
                """
                
                return "Dados atualizados com sucesso."
            elif (not isNewData and isExistWPensar == 0): #False and False
                """
                A informação não é nova e não está cadastrada na plataforma
                """
                # if data['nomeAluno'] == 'Aluno teste Leonardo':
                #     teste = dataAluno(data.to_dict())
                    # print(self.WPensar.accessPoint.updateData(dataJson = teste.toJson()))
                return "Incluir manualmente."
            else:
                return "Erro"
        else:
            return "Documento não finalizado ou é teste"

    def sendDataToWPensar(self, target, data):        
        pk = 'new'
        if target == 'alunos':
            dataTreated = dataAluno(data.to_dict())
            if data['matriculaWPensar'] != 0:
                pk = data['matriculaWPensar']
        elif target == 'responsaveis':
            dataTreated = dataResponsavel(data.to_dict())
            if data['codigoResponsavel'] != 0:
                pk = data['matriculaWPensar']
        else:
            pass
        print(pk)
        return self.WPensar.accessPoint.updateData(pk = pk, dataJson = dataTreated.toJson(), target = target) if dataTreated else None


    def doAllIncludes(self):
        # self.dataframeStatus = self.ClickSign.copy() if self.dataframeStatus is None else self.dataframeStatus
        tqdm.pandas()
        """
        Incluir alunos
        """
        # print("Iniciando inclusão de alunos")
        # print("Buscando números de matrícula na WPensar...\n")
        # self.ClickSign['matriculaWPensar'] = self.ClickSign.progress_apply(lambda x: self.searchInWPensar(x['nomeAluno'], target='aluno'), axis = 1)
        # print("Confirmando qual o procedimento a ser adotado...\n")
        # # descomentar post
        # self.ClickSign['inclusaoAluno'] = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x), axis = 1)
        
        """
        Incluir responsáveis
        O número de responsáveis depende da planilha
        """
        print("Iniciando inclusão de responsáveis")
        if 'resp2_nome' in self.ClickSign.columns and 'resp_finc_nome' in self.ClickSign.columns:
            num_responsibles = 3
        elif 'resp1_nome' in self.ClickSign.columns and 'resp_finc_nome' in self.ClickSign.columns:
            num_responsibles = 2
        else:
            num_responsibles = 0
        print(f'Serão incluídos até {num_responsibles} responsáveis')

        print("Buscando os códigos dos responsáveis na WPensar...\n")
        # Responsável Financeiro
        self.ClickSign['resp_finc_codigo'] = self.ClickSign.progress_apply(lambda x: self.searchInWPensar(x['resp_finc_nome'], target='responsaveis') if (x['resp_finc_nome'] != '') else 0, axis = 1)
        self.getDataResponsibleForInclusion(data = self.ClickSign, radical='resp_finc')
        
        self.ClickSign['resp_finc_procedimento'] = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x, target= 'responsaveis'), axis = 1)
        
        # if num_responsibles == 3:
        #     self.ClickSign['codResponsavelWPensar_1'] = self.ClickSign.progress_apply(lambda x: self.searchInWPensar(x['nomeAluno']), axis = 1)
        # print("Confirmando qual o procedimento a ser adotado...\n")
        # self.ClickSign['procedimentoResponsável_1'] = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x), axis = 1, target= 'responsaveis')


        import os
        import openpyxl     
        filename = os.path.join(os.path.dirname('__file__'), 'reports_folder', 'testSaveFiles.xls')
        self.ClickSign.to_excel(filename, engine= 'openpyxl')
              

    def getDataResponsibleForInclusion(self, data, radical = 'resp_fin  c'):
        try:
            data['codigoResponsavel'] = data[f'{radical}_codigo'] 
        except:
            data['codigoResponsavel'] = ""
        try:
            data['nomeResponsavel'] = data[f'{radical}_nome']
        except:
            data['nomeResponsavel'] = ""
        try:
            data['emailResponsavel'] = data[f'{radical}_email']
        except:
            data['emailResponsavel'] = ""
        try:
            data['cpfResponsavel'] = data[f'{radical}_cpf']
        except:
            data['cpfResponsavel'] = ""
        try:
            data['celularResponsavel'] = data[f'{radical}_tel_celular']
        except:
            data['celularResponsavel'] = ""
        try:
            data['sexoResponsavel'] = data[f'{radical}_sexo']
        except:
            data['sexoResponsavel'] = ""
        try:
            data['dataNascimentoResponsavel'] = data[f'{radical}_dt_nascimento']
        except:
            data['dataNascimentoResponsavel'] = ""
        try:
            data['estadoCivilResponsavel'] = data[f'{radical}_estadoCivil']
        except:
            data['estadoCivilResponsavel'] = ""
        try:
            data['nacionalidadeResponsavel'] = data[f'{radical}_nacionalidade']
        except:
            data['nacionalidadeResponsavel'] = ""
        try:
            data['profissaoResponsavel'] = data[f'{radical}_profissao']
        except:
            data['profissaoResponsavel'] = ""
        try:
            data['identidadeResponsavel'] = data[f'{radical}_rg']
        except:
            data['identidadeResponsavel'] = ""
        try:
            data['telefoneResponsavel'] = data[f'{radical}_tel_residencial']
        except:
            data['telefoneResponsavel'] = ""
        try:
            data['cepResponsavel'] = data[f'{radical}_cep']
        except:
            data['cepResponsavel'] = ""
        try:
            data['logradouroResponsavel'] = data[f'{radical}_logradouro']
        except:
            data['logradouroResponsavel'] = ""
        try:
            data['numlogradouroResponsavel'] = data[f'{radical}_numero']
        except:
            data['numlogradouroResponsavel'] = ""
        try:
            data['complementoResponsavel'] = data[f'{radical}_complemento']
        except:
            data['complementoResponsavel'] = ""
            



class You(object):
    def __init__(self):
        print("You:: Whoa! Marriage arrangements?")

    def askInclusionManager(self):
        print("You:: Let's contact the event manager\n\n")
        em = InclusionManager()
        em.doAllIncludes()

    def __del__(self):
        print("You:: Thanks to Event Manager!\n\n")


