import pandas as pd
from designPartners.singleton import *
from accessWPensar.accessWPensar import *

class DataBaseWPensar(metaclass = MetaSingleton):
    # get all data to include in WPensar
    def __init__(self):
        self.accessPoint = wPensarAccessPoint()
        self.alunos = False
        self.responsaveis = False
        self.alunosResponsaveis = False
        self.getAllInformations()
        
    def getInformations(self, target="alunos"):
        import os
        filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '01_tests', 'backup', 'alunos','backup_20211029_19:59:52.json')
        try:
            # data = self.accessPoint.getInformations(pk='All', target=target)
            # descomentar as linhas acima para voltar a buscar na WPensar
            
            with open(filename) as json_data:
                data = json.load(json_data)
            dataframe = pd.DataFrame.from_records(data)
            return dataframe
        except:
            print('Ocorreu um erro durante a importação dos dados. Tente novamente mais tarde.')
            return False

    def getLoop(self, function, information):
        loopContinue = False
        while loopContinue == False:
            try:
                print(information)
                data = function
                loopContinue = True
                print('Operação concluída com sucesso.')
            except:
                print('Ocorreu um erro, repetindo o procedimento...')
                loopContinue = False
        return data

    def getAllInformations(self):
        self.alunos = self.getLoop(self.getInformations('alunos'), 'Buscando informações de alunos na WPensar...')
        # self.responsaveis = self.getLoop(self.getInformations('responsaveis'), 'Buscando informações de responsáveis na WPensar...')
        # self.alunosResponsaveis = self.getLoop(self.getInformations('alunos-responsaveis'), 'Buscando relação entre alunos e responsáveis na WPensar...')

    