import pandas as pd
from designPartners.singleton import *
from accessWPensar.accessWPensar import *

class DataBaseWPensar(metaclass = MetaSingleton):
    # get all data to include in WPensar
    def __init__(self):
        self.accessPoint = wPensarAccessPoint()
        
    def getAlunosAllInformations(self):
        try:
            alunosAll = self.accessPoint.getInformations(pk='All', target="alunos")
            dataframe = pd.DataFrame.from_records(alunosAll)
            return dataframe
        except:
            print('Ocorreu um erro durante a importação dos dados. Tente novamente mais tarde.')
            return False