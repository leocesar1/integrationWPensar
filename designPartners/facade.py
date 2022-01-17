#! virtualenv/bin/env python
from math import nan
from accessWPensar.dataFrame import *
from manipulationCSV.dataFrame import *
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode

class DeletionManager(object):
    def __init__(self):
        print("Iniciando processo de inclusão dos alunos na plataforma WPensar \n")
        # self.getDataframeStatus()
        self.getTableWPensar()
    
    def getTableWPensar(self):
        self.WPensar = DataBaseWPensar()

    def doDelete(self):
        for row in self.WPensar.responsaveis[['nome', 'codigo']].to_numpy():
            if row[0] == "nan":
                # print(f"{row[1]} - {row[0]}")
                print(self.WPensar.accessPoint.deleteData(pk = row[1]))

class InclusionManager(object):
    def __init__(self):
        print("Iniciando processo de inclusão dos alunos na plataforma WPensar \n")
        # self.getDataframeStatus()
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

    def choiceFile(self):
        import os
        folder = os.path.join(os.path.dirname('__file__'), 'planilha_clicksign')
        files = [os.path.join(nome) for nome in os.listdir(folder)]
        print(f"""Escolha o número correspondente ao arquivo que deseja importar:\n""")
        for i in range(0, len(files)):
            print(f"[{i+1}] - {files[i]}")
        while True:
            choice = input(f"\nEscolha um número de 1 a {i+1} ou 0 para cancelar:")
            if int(choice) >= 1 and int(choice) <= i+1:
                return files[int(choice)-1]
            elif int(choice) > i+1:
                print("Número inválido")
            else:
                return False
        
        
         

    def getTableCSV(self):
        # import os
        nameFile = self.choiceFile()
        if nameFile == False:
            exit()
        filename = nameFile
        self.dataBaseClickSign = DataBaseClickSign(filename)
        self.ClickSign = self.dataBaseClickSign.dataframeTreated

    def getTableWPensar(self):
        self.WPensar = DataBaseWPensar()
        # self.saveBackupJson()

    def calculateSimilarity(self, text1, text2):
        import jellyfish as jf
        
        return jf.levenshtein_distance(''.join(text1.split()), ''.join(text2.split()))

    def stringComparation(self, text1, text2):
        try:
            similarity = self.calculateSimilarity(unidecode(text1.upper()), unidecode(text2.upper()))

            if similarity == 0:
                if unidecode(''.join(text1.upper().split())) == unidecode(''.join(text2.upper().split())):
                    return True   # The strings are the same
                else:
                    return False  # The strings aren't the same
            else:
                return False
        except:
            return False

    def searchInAtLastInclusions(self, data, target = 'alunos', radical =''):
        if target =='alunos':
            pass
        elif target == 'responsaveis':
            codResponsavel = False
            print(self.newResponsibles)
            print(data[f'{radical}_nome'])
            if data[f'{radical}_nome'] in self.newResponsibles:
                codResponsavel = self.newResponsibles[data[f'{radical}_nome']]
                print(codResponsavel)
            
            if type(codResponsavel) is not bool:
                return codResponsavel
            else:
                return 0
        elif target == 'alunos-responsaveis':
            pass
        else:
            return 0

    def searchInWPensar(self, data, target = 'alunos', radical =''):
        if target =='alunos':
            matricula = False
            for row in self.WPensar.alunos[['nome', 'matricula']].to_numpy():
                if self.stringComparation(data['nomeAluno'], row[0]):
                    matricula = row[1]
            if type(matricula) is not bool:
                return matricula
            else:
                return 0
        elif target == 'responsaveis':
            codResponsavel = False
            for row in self.WPensar.responsaveis[['nome', 'codigo']].to_numpy():
                if self.stringComparation(data[f'{radical}_nome'], row[0]):
                    codResponsavel = row[1]
            if type(codResponsavel) is not bool:
                return codResponsavel
            else:
                return 0
        elif target == 'alunos-responsaveis':
            codAluno = data['matriculaWPensar']
            codResponsavel = data[f'{radical}_codigo']
            codRelacao = False
            for row in self.WPensar.alunosResponsaveis[["id", "mataluno", "codresponsavel"]].to_numpy():
                if codAluno == row[1] and codResponsavel == row[2]:
                    codRelacao = row[0]
            if type(codRelacao) is not bool:
                return codRelacao
            else:
                return 0            
        else:
            return 0

    def doIncludeMatricula(self, data = None):
        try:
            
            return self.sendDataToWPensar(target='matriculas', data = data)['codigo'] if data['matriculaWPensar'] != 0 else 'A matricula não foi realizada'
        except:
            if not self.sendDataToWPensar(target='matriculas', data = data):   
                return 'O aluno já está na turma'
            else:
                return 'Erro'

    def doInclude(self, data = None, target = 'alunos', radical = ''):
        """
        This function returns pk number after consult or inclusion data at WPensar
        """
        data = self.ClickSign if data is None else data
        dontInsert = False
        if (data['finalizado'] or data['finalizado_manualmente']) and not data['teste']:
            # Busca a informação na tabela da clickSign
            if target == 'alunos':
                isNewData = data['novo_aluno']
                isExistWPensar = data['matriculaWPensar']
                returnData = 'matricula'
            elif target == 'responsaveis':
                if data[f'{radical}_nome'] == 'Primeiro Associado - Contratante':
                    radical = 'resp1'
                elif data[f'{radical}_nome'] == 'Segundo Associado - Contratante':
                    radical = 'resp2'
                dontInsert = True if data[f'{radical}_nome'] == 'Primeiro Associado - Contratante' or data[f'{radical}_nome'] == 'Segundo Associado - Contratante' else False
                isNewData = data['novo_responsavel']
                isExistWPensar = data[f'{radical}_codigo']
                returnData = 'codigo'
            elif target == 'alunos-responsaveis':
                isNewData = data['novo_responsavel']
                isExistWPensar = data[f'aluno_{radical}_codigo']
                returnData = 'id'
            else:
                return None
            # Verifica nos dados importados na WPensar
            
            if (isNewData and isExistWPensar != 0): #True and True
                """
                Apesar de ser considerada uma nova entrada,
                o dado já existe na plataforma
                retornaremos seu id
                """
                # print('1')
                try:
                    return [self.sendDataToWPensar(target=target, data = data, radical = radical)[f'{returnData}'], "Dados atualizados."] if not dontInsert else [0, f"Será inserido como {data['nomeResponsavel']}"]
                except:
                    return [0, "Erro 1"]
            elif (isNewData and isExistWPensar == 0): #True and False
                '''
                A informação é nova e ainda não foi inserido na plataforma
                Após a inclusão, retornaremos seu id
                '''
                # print('2')
                response = self.sendDataToWPensar(target=target, data = data, radical = radical)
                try: 
                    return [response[f'{returnData}'], "Dados inseridos."] if not dontInsert else [0, f"Será inserido como {data['nomeResponsavel']}"]
                except:
                    return [0, "Relação já existente na WPensar"]

            elif (not isNewData and isExistWPensar != 0): #False and True
                """
                A informação já existe na plataforma
                retornaremos seu id
                """
                response = self.sendDataToWPensar(target=target, data = data, radical = radical)
                try:
                    return [response[f'{returnData}'], "Dados atualizados."] if not dontInsert else [0, f"Será inserido como {data['nomeResponsavel']}"]
                except:
                    return [0, "Relação já existente na WPensar"]
            elif (not isNewData and isExistWPensar == 0): #False and False
                """
                A informação não é nova e não está cadastrada na plataforma
                """
                return [0, "Incluir manualmente."] if not dontInsert else [0, f"Será inserido como {data['nomeResponsavel']}"]
            else:
                return [0, "Erro 2"]
        else:
            return [0, "Documento não finalizado ou é teste"]

    def sendDataToWPensar(self, target, data, radical = ''):        
        pk = 'new'
        if target == 'alunos':
            dataTreated = dataAluno(data.to_dict())
            if data['matriculaWPensar'] != 0:
                pk = data['matriculaWPensar']
        elif target == 'responsaveis':
            dataTreated = dataResponsavel(data.to_dict(), radical = radical)
            if data[f'{radical}_codigo'] != 0:
                pk = data[f'{radical}_codigo']
            print(data[f'{radical}_codigo'])
        elif target == 'alunos-responsaveis':
            dataTreated = dataAlunoResponsavel(data.to_dict(), radical = radical)
            if data[f'aluno_{radical}_codigo'] != 0:
                pk = data[f'aluno_{radical}_codigo']
        elif target == 'matriculas':
            dataTreated = dataMatricula(data.to_dict())
        else:
            pass
        return self.WPensar.accessPoint.updateData(pk = pk, dataJson = dataTreated.toJson(), target = target) if dataTreated else None


    def doAllIncludes(self):
        tqdm.pandas()
        """
        Incluir alunos
        """
        print("\n\nIniciando inclusão de alunos")
        print("Buscando números de matrícula na WPensar...\n")
        self.ClickSign['matriculaWPensar'] = self.ClickSign.progress_apply(
            lambda x: self.searchInWPensar(x, target='alunos'), axis = 1)
        print("\n\nConfirmando qual o procedimento a ser adotado...\n")
        inclusion = self.ClickSign.progress_apply(
            lambda x: self.doInclude(data = x), axis = 1)
        self.ClickSign['matriculaWPensar'], self.ClickSign['inclusaoAluno'] = inclusion.progress_apply(lambda x: x[0]), inclusion.progress_apply(lambda x: x[1]) 

        """
        Matricular alunos
        """
        print("\n\nInserindo as matrículas")
        self.ClickSign['matriculaTurma'] = self.ClickSign.progress_apply(lambda x: self.doIncludeMatricula(x), axis = 1)
        

        """
        Incluir responsáveis
        O número de responsáveis depende da planilha
        """
        list_responsibles = ['resp1']
        list_responsibles.append('resp_finc') if 'resp_finc_nome' in self.ClickSign.columns else ''
        list_responsibles.append('resp2') if 'resp2_nome' in self.ClickSign.columns else ''

        self.newResponsibles = {}
        # self.setNewDataColumnsForResponsibles()
        print("\n\nIniciando inclusão de responsáveis...")
        
        for radical in list_responsibles:
            self.ClickSign[f'{radical}_codigo'], self.ClickSign[f'{radical}_procedimento'] = 0, 0
            self.ClickSign[f'aluno_{radical}_codigo'], self.ClickSign[f'aluno_{radical}_procedimento'] = 0, 0
            # Responsável Financeiro, Responsável 1 e (talvez) Responsável 2
            printProgressBar(0, len(self.ClickSign), prefix=f'Inserindo {radical}:',
                                suffix='Completo', length=50)
            for index, row in self.ClickSign.iterrows():
                # 1- Verificar na WPensar
                codigo = self.searchInWPensar(row, target='responsaveis', radical = radical) if (row[f'{radical}_nome'] != '') else 0
                if codigo != 0:
                    pass
                else:
                # 2- Verificar se já foi incluída
                    codigo = self.searchInAtLastInclusions(row, target='responsaveis', radical = radical) if (row[f'{radical}_nome'] != '' and row[f'{radical}_nome']!= 'Primeiro Associado - Contratante' and row[f'{radical}_nome']!= 'Segundo Associado - Contratante') else 0
                # 3 - Define a variável
                self.ClickSign.loc[index, f'{radical}_codigo'] = codigo
                row[f'{radical}_codigo'] = codigo
                
                # print(self.ClickSign.loc[index, f'{radical}_codigo'])
                # print(row[f'{radical}_codigo'])

                self.ClickSign.loc[index, f'aluno_{radical}_codigo'] = self.searchInWPensar(row, target='alunos-responsaveis', radical = radical) if (row[f'{radical}_codigo'] != 0) else 0
                row[f'aluno_{radical}_codigo'] = self.searchInWPensar(row, target='alunos-responsaveis', radical = radical) if (row[f'{radical}_codigo'] != 0) else 0
                # 3- Inserir e retornar inclusão
                # self.getDataResponsibleForInclusion(index, data = row, radical=f'{radical}')
                # self.getDataStudentResponsibleForInclusion(index, data = self.ClickSign, radical=f'{radical}')

                self.ClickSign.loc[index,f'{radical}_codigo'], self.ClickSign.loc[index,f'{radical}_procedimento'] = self.doInclude(data = row, target= 'responsaveis', radical = radical)
                
                self.ClickSign.loc[index, f'aluno_{radical}_codigo'], self.ClickSign.loc[index, f'aluno_{radical}_procedimento'] = self.doInclude(data = row, target= 'alunos-responsaveis', radical = radical)  
                

                if self.ClickSign.loc[index, f'{radical}_codigo'] != 0:
                    self.newResponsibles[self.ClickSign.loc[index, f'{radical}_nome']] = int(self.ClickSign.loc[index, f'{radical}_codigo'])
                    
                printProgressBar(index+1, len(self.ClickSign), prefix=f'Inserindo {radical}:',
                                    suffix='Completo', length=50)

            # Responsável Financeiro, Responsável 1 e (talvez) Responsável 2
            # print(f"\nBuscando os códigos dos responsáveis no campo {radical}...")
            # self.ClickSign[f'{radical}_codigo'] = self.ClickSign.progress_apply(lambda x: self.searchInWPensar(x, target='responsaveis', radical = radical) if (x[f'{radical}_nome'] != '') else 0, axis = 1)
            # self.getDataResponsibleForInclusion(data = self.ClickSign, radical=f'{radical}')
            # print(f"Incluindo responsáveis no campo {radical}...")
            # inclusion = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x, target= 'responsaveis'), axis = 1)
            # self.ClickSign[f'{radical}_codigo'], self.ClickSign[f'{radical}_procedimento'] = inclusion.progress_apply(lambda x: x[0]), inclusion.progress_apply(lambda x: x[1]) 
            

            # print(f"\nBuscando relação entre responsável do campo {radical} e aluno...")
            # self.ClickSign[f'aluno_{radical}_codigo'] = self.ClickSign.progress_apply(lambda x: self.searchInWPensar(x, target='alunos-responsaveis', radical = radical) if (x[f'{radical}_codigo'] != 0) else 0, axis = 1)
            # self.getDataStudentResponsibleForInclusion(data = self.ClickSign, radical=f'{radical}')
            # print(f"\nInserindo relação entre responsável do campo {radical} e aluno...")
            # inclusion = self.ClickSign.progress_apply(lambda x: self.doInclude(data = x, target= 'alunos-responsaveis'), axis = 1)
            # self.ClickSign[f'aluno_{radical}_codigo'], self.ClickSign[f'aluno_{radical}_procedimento'] = inclusion.progress_apply(lambda x: x[0]), inclusion.progress_apply(lambda x: x[1]) 
        self.saveBackupResults()


    def saveBackupResults(self):
        import os, datetime
        # import openpyxl     
        filename = os.path.join(os.path.dirname('__file__'), 'reports_folder', f'ResultIntegrations_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.xls')
        self.ClickSign.to_excel(filename, engine= 'openpyxl')

    
        
              
    # def getDataStudentResponsibleForInclusion(self,index, data, radical = 'resp_fin  c'):
    #     try:
    #         data.loc[index,'codigoAlunoResponsavel'] = data[f'aluno_{radical}_codigo'] 
    #     except:
    #         data.loc[index,'codigoAlunoResponsavel'] = ""

    # def setNewDataColumnsForResponsibles(self):
        # self.ClickSign['codigoResponsavel'] = ""
        # self.ClickSign['nomeResponsavel'] = ""
        # self.ClickSign['emailResponsavel'] = ""
        # self.ClickSign['cpfResponsavel'] = ""
        # self.ClickSign['celularResponsavel'] = ""
        # self.ClickSign['sexoResponsavel'] = ""
        # self.ClickSign['dataNascimentoResponsavel'] = ""
        # self.ClickSign['estadoCivilResponsavel'] = ""
        # self.ClickSign['nacionalidadeResponsavel'] = ""
        # self.ClickSign['profissaoResponsavel'] = ""
        # self.ClickSign['identidadeResponsavel'] = ""
        # self.ClickSign['telefoneResponsavel'] = ""
        # self.ClickSign['cepResponsavel'] = ""
        # self.ClickSign['logradouroResponsavel'] = ""
        # self.ClickSign['numlogradouroResponsavel'] = ""
        # self.ClickSign['complementoResponsavel'] = ""
        # self.ClickSign['codigoAlunoResponsavel'] = ""


    def getDataResponsibleForInclusion(self, index, data, radical = 'resp_finc'):
        try:
            self.ClickSign.loc[index,'codigoResponsavel'] = data[f'{radical}_codigo']
        except:
            self.ClickSign.loc[index,'codigoResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'nomeResponsavel'] = data[f'{radical}_nome']
        except:
            self.ClickSign.loc[index, 'nomeResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'emailResponsavel'] = data[f'{radical}_email']
        except:
            self.ClickSign.loc[index, 'emailResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'cpfResponsavel'] = data[f'{radical}_cpf']
        except:
            self.ClickSign.loc[index, 'cpfResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'celularResponsavel'] = data[f'{radical}_tel_celular']
        except:
            self.ClickSign.loc[index, 'celularResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'sexoResponsavel'] = data[f'{radical}_sexo']
        except:
            self.ClickSign.loc[index, 'sexoResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'dataNascimentoResponsavel'] = data[f'{radical}_dt_nascimento']
        except:
            self.ClickSign.loc[index, 'dataNascimentoResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'estadoCivilResponsavel'] = data[f'{radical}_estadoCivil']
        except:
            self.ClickSign.loc[index, 'estadoCivilResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'nacionalidadeResponsavel'] = data[f'{radical}_nacionalidade']
        except:
            self.ClickSign.loc[index, 'nacionalidadeResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'profissaoResponsavel'] = data[f'{radical}_profissao']
        except:
            self.ClickSign.loc[index, 'profissaoResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'identidadeResponsavel'] = data[f'{radical}_rg']
        except:
            self.ClickSign.loc[index, 'identidadeResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'telefoneResponsavel'] = data[f'{radical}_tel_residencial']
        except:
            self.ClickSign.loc[index, 'telefoneResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'cepResponsavel'] = data[f'{radical}_cep']
        except:
            self.ClickSign.loc[index, 'cepResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'logradouroResponsavel'] = data[f'{radical}_logradouro']
        except:
            self.ClickSign.loc[index, 'logradouroResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'numlogradouroResponsavel'] = data[f'{radical}_numero']
        except:
            self.ClickSign.loc[index, 'numlogradouroResponsavel'] = ""
        try:
            self.ClickSign.loc[index, 'complementoResponsavel'] = data[f'{radical}_complemento']
        except:
            self.ClickSign.loc[index, 'complementoResponsavel'] = ""
            



class You(object):
    def __init__(self):
        import time
        print("Iniciando inclusões no sistema WPensar", end="",flush=True)
        # for i in range(2):
        #     time.sleep(1)
        #     print('.',end="", flush=True)
        # print('.')
        # time.sleep(1)

    def askInclusionManager(self):
        # print("You:: Let's contact the event manager\n\n")
        em = InclusionManager()
        em.doAllIncludes()

    def __del__(self):
        print("Processo finalizado!!!")
    
    def deleteNanResponsible(self):
        em = DeletionManager()
        em.doDelete()



