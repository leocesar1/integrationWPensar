


# Load clicksign spreadsheet
from manipulationCSV.dataFrame import *

# dataBaseClickSign = DataBaseClickSign('Relatório - matrículas internas.csv')
# dataBaseClickSign = DataBaseClickSign('Relatório -matrículas internas excepcionais.csv')
# dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas.csv')
dataBaseClickSign = DataBaseClickSign('Relatório - matrículas externas - excepcionais.csv')
# a = dataBaseClickSign.dataframeOriginal
# d = dataBaseClickSign.dataframeTreated
# print(d.columns.values.tolist())
# print(d['situacao'])
dataBaseClickSign.saveAsXls()
# Load WPensar json
# from accessWPensar.dataFrame import *

# dataBaseWPensar = DataBaseWPensar()


# # is a draft for a loop verification
# text2 = dataBaseWPensar.alunos['nome']

# for i in range(0,len(dataBaseClickSign.getAlunoData(dataBaseClickSign.dataframeRenovations))):
#     text1 = dataBaseClickSign.getAlunoData(dataBaseClickSign.dataframeRenovations).iloc[i,0]
#     for item in text2:
#         if dataBaseWPensar.stringComparation(text1, item):
#             print(item)