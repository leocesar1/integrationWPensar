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
        self.dataBaseClickSign = DataBaseClickSign('Relatório - matrículas internas.csv')
        
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

    def searchStudentInWPensar(self, text1):
        matricula = False
        for row in self.WPensar.alunos[['nome', 'matricula']].to_numpy():
            if self.stringComparation(text1, row[0]):
                matricula = row[1]
        if type(matricula) is not bool:
            # print(f"{matricula}: {text1}")
            return matricula
        else:
            return 0

    def doInclude(self, data = None, target = 'alunos'):
        """
        This function returns pk number after consult or inclusion data at WPensar
        """
        data = self.ClickSign if data is None else data
        
        if target == 'alunos' and data['status'] == "Finalizado" and not data['teste']:
            # Busca a informação de novo aluno na tabela da clickSign
            isNewStudent = data['novo_aluno']
            # Verifica nos dados importados na WPensar
            isExistWPensar = data['matriculaWPensar']
            # print("\nIniciando inclusão de alunos...")
            if (isNewStudent and isExistWPensar != 0): #True and True
                """
                Apesar de ser considerado novo alunos,
                o aluno já existe na plataforma
                retornaremos o id do aluno
                """
                
                return "Aluno novo, porém já existe na WPensar - Apenas atualizar os dados"
            elif (isNewStudent and isExistWPensar == 0): #True and False
                '''
                O aluno é novo e ainda não foi inserido na plataforma
                Após a inclusão, retornaremos o id do aluno
                '''
                
                return "Aluno novo, não existe na WPensar - Cadastrar novos dados"
            elif (not isNewStudent and isExistWPensar != 0): #False and True
                """
                O aluno já existe na plataforma
                retornaremos o id do aluno
                """
                
                return "Aluno antigo, já existe na WPensar - Apenas atualizar os dados"
            elif (not isNewStudent and isExistWPensar == 0): #False and False
                """
                O aluno não é novo e não está cadastrado na plataforma
                """
                if data['nomeAluno'] == 'Aluno teste Leonardo':
                    teste = dataAluno(data.to_dict())
                    # print(teste.toJson())
                    # print(self.WPensar.accessPoint.updateData(dataJson = teste.toJson()))
                return "Aluno antigo, porém não foi encontrado na WPensar - Listar para futuras inclusões manuais"
            else:
                return "Erro"
        else:
            return "Documento não finalizado ou é teste"
                
    def doAllIncludes(self):
        # self.dataframeStatus = self.ClickSign.copy() if self.dataframeStatus is None else self.dataframeStatus
        tqdm.pandas()
        print("Iniciando inclusão de alunos")
        print("Buscando números de matrícula na WPensar...\n")
        self.ClickSign['matriculaWPensar'] = self.ClickSign.progress_apply(lambda x: self.searchStudentInWPensar(x['nomeAluno']), axis = 1)
        print("Confirmando qual o procedimento a ser adotado...\n")
        self.ClickSign['procedimento'] = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x), axis = 1)
        
        import os
        import xlwt     
        filename = os.path.join(os.path.dirname('__file__'), 'reports_folder', 'testSaveFiles.xls')
        self.ClickSign.to_excel(filename)
              





class You(object):
    def __init__(self):
        print("You:: Whoa! Marriage arrangements?")

    def askInclusionManager(self):
        print("You:: Let's contact the event manager\n\n")
        em = InclusionManager()
        em.doAllIncludes()

    def __del__(self):
        print("You:: Thanks to Event Manager!\n\n")


