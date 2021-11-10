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
        try:
            data = self.accessPoint.getInformations(pk='All', target=target)
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
        self.responsaveis = self.getLoop(self.getInformations('responsaveis'), 'Buscando informações de responsáveis na WPensar...')
        self.alunosResponsaveis = self.getLoop(self.getInformations('alunos-responsaveis'), 'Buscando relação entre alunos e responsáveis na WPensar...')

    def calculateSimilarity(self, text1, text2):
        import jellyfish as jf
        
        return jf.levenshtein_distance(''.join(text1.split()), ''.join(text2.split()))

    def stringComparation(self, text1, text2):
        if self.calculateSimilarity(text1.upper(), text2.upper()) == 0:
            if ''.join(text1.upper().split()) == ''.join(text2.upper().split()):
                return True   # The strings are the same
            else:
                return False  # The strings aren't the same